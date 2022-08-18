from enum import Enum
from typing import Tuple, Union, Optional, Dict, List

from FoxDot.lib.TimeVar import TimeVar
from pprint import pformat

class ReaTrackType(Enum):
    INSTRUMENT = 1
    BUS = 2

def make_snake_name(name: str) -> str:
    return name.lower().replace(' ', '_').replace('/', '_').replace('(', '_').replace(':', '_').replace('__','_').replace('-','_')

def split_param_name(name) -> Tuple[str, str]:
    if name == make_snake_name(name):
        splitted = name.split('_')
        reaobject_name = splitted[0]
        param_name = '_'.join(splitted[1:])
        return reaobject_name, param_name
    else:
        raise KeyError("Parameter name not snake_case :" + name)

class ReaTask(object):
    def __init__(self, type, reaper_object, param_name, param_value):
        self.id = id(self)
        self.type = type
        self.reaper_object = reaper_object
        self.param_name = param_name
        self.param_value = param_value
        self.result = None

class ReaParamState(Enum):
    NORMAL = 0
    VAR1 = 1
    VAR2 = 2

class ReaParam(object):
    def __init__(self, name, value, index=None, reaper_name=None, state=ReaParamState.NORMAL):
        self.name = name
        self.index = index
        self.value = value
        self.reaper_name = reaper_name
        self.state: ReaParamState = state

class ReaSend(ReaParam):
    def __repr__(self):
        return "<ReaSend {}>".format(self.name)

class ReaTrack(object):
    def __init__(self, clock, track, name: str, type: ReaTrackType, reaproject):
        self._clock = clock
        self.track = track
        self.reaproject = reaproject
        self.name = name
        self.type = type
        self.reafxs = {}
        self.firstfx = None
        self.preset = None
        self.reaparams: Dict[str, ReaSend] = {}
        for index, send in enumerate(self.track.sends):
            name = make_snake_name(send.dest_track.name)[1:]
            if name =="mixer":
                self.reaparams["vol"] = ReaSend(name=name, index=index, value=send.volume*2)
            else:
                self.reaparams[name] = ReaSend(name=name, index=index, value=send.volume)
        for index, fx in enumerate(self.track.fxs):
            snake_name = make_snake_name(fx.name)
            if index == 0 and self.firstfx is None:
                self.firstfx = snake_name
            if snake_name not in self.reafxs.keys():
                reafx = ReaFX(fx, snake_name, index)
                self.reafxs[snake_name] = reafx
            elif isinstance(self.reafxs[snake_name], ReaFXGroup):
                self.reafxs[snake_name].add_fx_to_group(fx, index)
            else:
                old_reafx = self.reafxs[snake_name]
                reafxgroup = ReaFXGroup([old_reafx.fx, fx], snake_name, [old_reafx.index, index])
                self.reafxs[snake_name] = reafxgroup

    def __repr__(self):
        return "<ReaTrack {} - {}>".format(self.name, pformat(self.reafxs))

    def create_reafx(self, plugin_name: str, plugin_preset: str=None, reafx_name: str=None, param_alias_dict: Dict={}, scan_all_params=False):
        if reafx_name is None:
            reafx_name = make_snake_name(plugin_name)
        if not self.reafxs and self.firstfx is None:
            self.firstfx = reafx_name
        # add fx in last position : the index is len of the fx list - 1
        with self.reaproject.reapylib.inside_reaper():
            fx = self.track.add_fx(plugin_name)
            if plugin_preset is not None: # plugin preset in reaper has to be applied first (before ReaFX obj creation) as it changes existing parameters
                fx.preset = plugin_preset
                self.preset = plugin_preset
            reafx = ReaFX(fx, reafx_name, len(self.reafxs.keys()) - 1, param_alias_dict, scan_all_params)
            self.reafxs[reafx_name] = reafx
            return reafx

    def delete_reafx(self, fx_index, reafx_name):
        self.track.fxs[fx_index].delete()
        del self.reafxs[reafx_name]

    def get_param(self, full_name):
        if full_name in self.reaparams.keys():
            return self.reaparams[full_name].value
        else:
            fx_name, param_name = split_param_name(full_name)
            return self.reafxs[fx_name].reaparams[param_name].value

    def get_all_params(self):
        result = {send.name: send.value for send in self.reaparams.values()}
        for reafx in self.reafxs.values():
            result = result | reafx.get_all_params()
        return result

    def set_param(self, name, value):
        # if name == "mixer":
        #     name = "vol"
        # name = "vol" if name =="mixer" else name
        # value = value/2 if name =="vol" else value
        self.reaparams[name].value = value

    def set_param_direct(self, name, value):
        value = value/2 if name =="vol" else value
        param = self.reaparams[name]
        self.track.sends[param.index].volume = 5*float(value)**2.5 # convert vol logarithmic value to linear 0 -> 1 value




class ReaFX(object):
    def __init__(self, fx, name, index, param_alias_dict={}, scan_all_params=True):
        self.fx = fx
        self.name = name
        self.index = index
        self.reaparams: Dict[str, ReaParam] = {}
        self.reaparams['on'] = ReaParam(name='on', value=fx.is_enabled, index=-1)
        if scan_all_params:
            for index, param in enumerate(fx.params):
                if param.name in param_alias_dict.keys():
                    param_alias = make_snake_name(param_alias_dict[param.name])
                    param_reaper_name = param.name
                else:
                    param_alias = make_snake_name(param.name)
                    param_reaper_name = param.name
                self.reaparams[param_alias] = ReaParam(name=param_alias, value=param.real, index=index, reaper_name=param_reaper_name)
        else:
            for param_name in param_alias_dict.keys():
            #selected_params = [param for param in fx.params if param.name in param_alias_dict.keys()]
            #for index, param in enumerate(selected_params):
                try:
                    #param_name = param.name
                    param = fx.params[param_name]
                    #if param_name in param_alias_dict.keys():
                    param_alias = make_snake_name(param_alias_dict[param_name])
                    param_reaper_name = param.name
                    self.reaparams[param_alias] = ReaParam(name=param_alias, value=param.real, index=param.index,
                                                           reaper_name=param_reaper_name)
                except:
                    print(f"Param with name {param_name} does not exist in Reaper FX {name}")
                    print(f"Existing params : {[param.name for param in fx.params]}")

    def __repr__(self):
        return "<ReaFX {}>".format(self.name)

    def get_all_params(self):
        return {self.name + "_" + param.name : param.value for param in self.reaparams.values()}

    def get_param(self, name):
        return self.reaparams[name].value

    def set_param(self, name, value):
        self.reaparams[name].value = value

#    def set_param_direct(self, name, value):
#        if name == "on":
#            if not value:
#                self.fx.disable()
#            else:
#                self.fx.enable()
#        else:
#            reaper_name = self.reaparams[name].reaper_name
#            try:
#                self.fx.params[reaper_name] = float(value)
#                print(f"set param direct: {name} {reaper_name} {value}")
#            except:
#                print(f"error set param direct: {name} {reaper_name} {value}")


    def set_param_direct(self, name, value):
        if name == "on":
            if not value:
                self.fx.disable()
            else:
                self.fx.enable()
        else:
            id = self.reaparams[name].index
            self.fx.params[id] = float(value)


class ReaFXGroup(ReaFX):
    def __init__(self, fxs, name, indexes:List[int]):
        self.fxs = fxs
        self.name = name
        self.indexes = indexes
        self.reaparams: Dict[str, ReaParam] = {}
        self.reaparams['on'] = ReaParam(name='on', value=fxs[0].is_enabled, index=-1)
        for index, param in enumerate(fxs[0].params):
            snake_name = make_snake_name(param.name)
            self.reaparams[snake_name] = ReaParam(name=snake_name, value=param.real, index=index)

    def add_fx_to_group(self, fx, index):
        self.fxs.append(fx)
        self.indexes.append(index)

    def __repr__(self):
        return "<ReaFXGroup {}>".format(self.name)

    def set_param_direct(self, name, value):
        if name == "on":
            for fx in self.fxs:
                if not value:
                    fx.disable()
                else:
                    fx.enable()
        else:
            id = self.reaparams[name].index
            for fx in self.fxs:
                fx.params[id] = float(value)


class ReaProject(object):
    def __init__(self, clock, reapylib):
        self._clock = clock
        self.reapy_project = reapylib.Project()
        self.reatracks = {}
        self.reapylib = reapylib
        self.instrument_tracks = []
        self.bus_tracks = []
        self.reapy_access_tasks = []
        self.reapy_access_queue_size = 200
        self.reapy_task_execute_freq = 0.1
        self.reapy_results_by_id = {}
        self.currently_processing_tasks = False
        self.clearing_task_queue = False
        with reapylib.inside_reaper():
            for index, track in enumerate(self.reapy_project.tracks):
                snake_name: str = make_snake_name(track.name)
                reatrack = ReaTrack(self._clock, track, name=snake_name, type=ReaTrackType.INSTRUMENT, reaproject=self)
                self.reatracks[snake_name] = reatrack
                if snake_name.startswith('_'):
                    self.bus_tracks.append(reatrack)
                else:
                    self.instrument_tracks.append(reatrack)

    def __repr__(self):
        return "<ReaProject \n\n ################ \n\n {}>".format(self.reatracks)

    def get_track(self, track_name):
        return self.reatracks[track_name]

    def clear_tasks(self, value=True):
        self.clearing_task_queue = value
        #self._clock.future(4, self.clear_tasks, args=[False])  # add autodeactivation
        self.reapy_access_tasks = []

    def add_reapy_task(self, task: ReaTask):
        if len(self.reapy_access_tasks) < self.reapy_access_queue_size and not self.clearing_task_queue:
            self.reapy_access_tasks.append(task)
            if not self.currently_processing_tasks:
                self._clock.future(self.reapy_task_execute_freq, self.execute_reapy_tasks, args=[])
        else:
            print("maximum reapy tasks in queue reached")

    def execute_reapy_tasks(self):
        if not self.currently_processing_tasks:
            self.currently_processing_tasks = True
            with self.reapylib.inside_reaper():
                while self.reapy_access_tasks:
                    task: ReaTask = self.reapy_access_tasks.pop(0)
                    if task.type == "set":
                        task.reaper_object.set_param_direct(task.param_name, task.param_value)
                        task.reaper_object.set_param(task.param_name, task.param_value)
            self.currently_processing_tasks = False
            if not self.clearing_task_queue:
                self._clock.future(self.reapy_task_execute_freq, self.execute_reapy_tasks, args=[])

    def timevar_update_loop(self, rea_object, name, value, state, update_freq):
        if rea_object.reaparams[name].state == state:
            self.add_reapy_task(ReaTask("set", rea_object, name, value))
            self._clock.future(update_freq, self.timevar_update_loop, args=[rea_object, name, value, state, update_freq])

def get_reaper_object_and_param_name(track: ReaTrack, param_fullname: str, quiet: bool = True)\
        -> Tuple[Optional[Union[ReaTrack, ReaFX]], Optional[str]]:
    """
    Return object (ReaTrack or ReaFX) and parameter name to apply modification to.
    Choose usecase (parameter kind : track param like vol, send amount or fx param) depending on parameter name.
    """
    reaper_object, param_name = None, None
    # Param concern current track (it is a reaper send)
    if param_fullname in track.reaparams.keys():
        reaper_object = track
        return reaper_object, param_fullname
    # Param is a fx param
    elif '_' in param_fullname:
        fx_name, rest = split_param_name(param_fullname)
        if fx_name in track.reafxs.keys():
            fx = track.reafxs[fx_name]
            if rest in fx.reaparams.keys() or rest == 'on':
                reaper_object = track.reafxs[fx_name]
                param_name = rest
                return reaper_object, param_name
    elif param_fullname in track.reafxs[track.firstfx].reaparams.keys(): # Try to match param name with first fx params
        reaper_object = track.reafxs[track.firstfx]
        return reaper_object, param_fullname
    if not quiet:
        print("Parameter doesn't exist: " + param_fullname)
    return reaper_object, param_name


def set_reaper_param(track: ReaTrack, full_name, value, update_freq=.1):
    # rea_object can point to a fx or a track (self) -> (when param is vol or other send)
    rea_object, name = get_reaper_object_and_param_name(track, full_name)

    # If object not found abort
    if rea_object is None or name is None:
        return

    # If we set an fx param turn the fx on
    if isinstance(rea_object, ReaFX) or isinstance(rea_object, ReaFXGroup):
        if name != 'on':
            track.reaproject.add_reapy_task(ReaTask("set", rea_object, 'on', True))

    # handle switching between time varying (setup recursion loop to update value in the future) or non varying params (normal float)
    if isinstance(value, TimeVar) and name != 'on':
        # to update a time varying param and tell the preceding recursion loop to stop
        # we switch between two timevar state old and new alternatively 'timevar1' and 'timevar2'
        if rea_object.reaparams[name].state != ReaParamState.VAR1:
            new_state = ReaParamState.VAR1
        else:
            new_state = ReaParamState.VAR2
        def initiate_timevar_update_loop(name, value, new_state, update_freq):
            rea_object.reaparams[name].state = new_state
            track.reaproject.timevar_update_loop(rea_object, name, value, new_state, update_freq)
        # beat=None means schedule for the next bar
        track._clock.schedule(initiate_timevar_update_loop, beat=None, args=[name, value, new_state, update_freq])
    else:
        # to switch back to non varying value use the state normal to make the recursion loop stop
        def normal_value_update(rea_object, name, value):
            rea_object.reaparams[name].state = ReaParamState.NORMAL
            rea_object.set_param(name, float(value))
            track.reaproject.add_reapy_task(ReaTask("set", rea_object, name, float(value)))
        # beat=None means schedule for the next bar
        track._clock.schedule(normal_value_update, beat=None, args=[rea_object, name, value])

def get_reaper_param(self, full_name):
    # rea_object can point to a fx or a track (self) -> (when param is vol or pan)
    rea_object, name = get_reaper_object_and_param_name(self, full_name)
    if rea_object is None or name is None:
        return None
    return rea_object.get_param(full_name)