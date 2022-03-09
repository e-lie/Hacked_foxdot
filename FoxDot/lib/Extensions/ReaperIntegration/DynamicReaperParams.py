from enum import Enum
from FoxDot.lib.TimeVar import TimeVar
from pprint import pprint, pformat
import reapy
import time

class ReaTrackType(Enum):
    INSTRUMENT = 1
    BUS = 2


def make_snake_name(name: str) -> str:
    return name.lower().replace(' ', '_').replace('/', '_').replace('(', '_').replace(':', '_').replace('__','_')

class ReaProject(object):

    def __init__(self, clock):
        self._clock = clock
        self.reapy_project = reapy.Project()
        self.reatracks = {}
        self.sends = {}
        self.reamaster = None
        self.sends_group = None
        self.instrument_tracks = []
        self.bus_tracks = []
        self.param_updates = []
        self.currently_processing_params = False
        self.param_update_freq = 0.05
        self.param_updates_queue_size = 50

        with reapy.inside_reaper():
            for id, track in enumerate(self.reapy_project.tracks):
                snake_name: str = make_snake_name(track.name)
                reatrack = ReaTrack(self._clock, name=snake_name, type=ReaTrackType.INSTRUMENT, track=track, reaproject=self)
                self.reatracks[snake_name] = reatrack
                if snake_name.startswith('_'):
                    self.bus_tracks.append(reatrack)
                else:
                    self.instrument_tracks.append(reatrack)

    def __repr__(self):
        return "<ReaProject {} \n\n ################ \n\n {}>".format(self.reatracks)

    def get_track(self, track_name):
        return self.reatracks[track_name]

    def add_param_update(self, device, name, value):
        if len(self.param_updates) < self.param_updates_queue_size:
            #print("add param update {}".format((device, name, value)))
            #print("processing params: {}".format(self.currently_processing_params))
            #print("queue size: {}".format(len(self.param_updates)))
            self.param_updates.append((device, name, value))
            if not self.currently_processing_params:
                # self.currently_processing_params = True
                #print("adding execute schedule from add param")
                self._clock.future(self.param_update_freq, self.execute_param_updates, args=[])
        else:
            print("maximum param updates reached")

    def execute_param_updates(self):
        #print("execute param updates: ")
        #print("processing params: {}".format(self.currently_processing_params))
        if not self.currently_processing_params:
            self.currently_processing_params = True
            with reapy.inside_reaper():
                while self.param_updates:
                    device, name, value = self.param_updates.pop(0)
                    print("processing {}".format((device, name, value)))
                    setattr(device, name, float(value))
            self.currently_processing_params = False
            #print("adding execute schedule from execute")
            self._clock.future(self.param_update_freq, self.execute_param_updates, args=[])

    def set_param_futureloop(self, device, name, value, state, update_freq):
        #print("set_param_futureloop {}".format((device, name, value)))
        if device.get_param_states()[name] == state:
            #with reapy.inside_reaper():
            #    setattr(device, name, float(value))
            self.add_param_update(device, name, value)
            self._clock.future(update_freq, self.set_param_futureloop, args=[device, name, value, state, update_freq])

    # def set_send_ids(self, send_ids):
    #     for track in self.reatracks.values():
    #         track.set_send_ids(send_ids)


class ReaTrack(object):

    send_ids = {}

    def __init__(self, clock, track, name: str, type: ReaTrackType, reaproject: ReaProject):
        self._clock = clock
        self.track = track
        self.reaproject = reaproject
        self.name = name
        self.type = type
        self.config = {}
        self.reafxs = {}
        self.reafx_list = []
        self.param_states = {}
        for id, fx in enumerate(self.track.fxs):
            snake_name = make_snake_name(fx.name)
            reafx = ReaFX(fx, snake_name)
            self.reafxs[snake_name] = reafx
            self.reafx_list.append(reafx)

    def __repr__(self):
        return "<ReaTrack {} - {}>".format(self.name, pformat(self.reafxs))

    def __getattr__(self, key):
        if key == "vol":
            return self.track.sends[0].volume
        elif key == "pan":
            return self.track.sends[0].pan
        return self.__dict__[key]

    def __setattr__(self, key, value):
        if key == "vol":
            self.track.sends[0].volume = value
        elif key == "pan":
            self.track.sends[0].pan = value
        else:
            self.__dict__[key] = value

    @classmethod
    def split_param_name(cls, name):
        if "_" in name:
            splitted = name.split('_')
            device_name = splitted[0]
            param_name = '_'.join(splitted[1:])
            return device_name, param_name
        else:
            raise KeyError("Parameter name not splittable by '_': " + name)

    # def getp(self):
    #     result = {}
    #     result["vol"] = self.vol
    #     result["pan"] = self.pan
    #     for name, send_num in self.reaproject.sends.items():
    #         result[name] = self.get_send(send_num)
    #     for name, smart_device in self.reafxs.items():
    #         result = result | smart_device.get_params()
    #     return result

    # @property
    # def vol(self):
    #     return float(self.track.volume) / 0.85
    #
    # @property
    # def pan(self):
    #     return self.track.pan

    def get_send(self, send_num):
        return self.track.sends(send_num).volume

    def set_send(self, send_num, value):
        self.track.sends(send_num).volume = value

    def get_reatrack(self):
        return self.track

    def get_param_states(self):
        return self.param_states

    def get_reaper_object_and_param_name(self, param_fullname: str, quiet: bool = True):
        """
        Return object (ReaTrack or ReaFX) and parameter name to apply modification to.
        Choose usecase (parameter kind : track param like vol, send amount or fx param) depending on parameter name.
        This is important to make parameter modification uniform for all cases.
        """
        # fx can point to a smart_device or a self (when param is vol or pan)
        reaper_object, param_name = None, None
        # Track vol or pan
        if param_fullname in ['vol', 'pan']:
            reaper_object = self
            param_name = param_fullname
            return reaper_object, param_name, param_fullname
        # Param is a send name
        elif "send_" in param_fullname:
            reaper_object = self
            param_name = param_fullname
            return reaper_object, param_name, param_fullname
        # Param is a fx param
        elif '_' in param_fullname:
            first_part, rest = ReaTrack.split_param_name(param_fullname)
            reafx_names = self.reafxs.keys()
            if first_part in reafx_names:
                fx = self.reafxs[first_part]
                param_names = fx.param_name_id_dict.keys()
                if rest in param_names:
                    reaper_object = self.reafxs[first_part]
                    param_name = rest
                    return reaper_object, param_name, param_fullname
        # If normal name split doesnt work use first fx (param name shortcut intru_i_param -> instru_param)
        elif self.reafx_list:
            first_device = self.reafx_list[0]
            param_names = first_device.param_name_id_dict.keys()
            if param_fullname in param_names:
                reaper_object = self.reafx_list[0]
                param_name = param_fullname
                return reaper_object, param_name, param_fullname
        if not quiet:
            print("Parameter doesn't exist: " + param_fullname)
        return reaper_object, param_name, param_fullname

    def set_reaper_param(self, full_name, value, update_freq=0.05):
        # fx can point to a fx or a track (self) -> (when param is vol or pan)
        rea_object, name, full_name = self.get_reaper_object_and_param_name(full_name)
        if rea_object is None or name is None:
            return

        self.config = self.config | {full_name: value}
        if isinstance(value, TimeVar):
            # to update a time varying param and tell the preceding recursion loop to stop
            # we switch between two timevar state old and new alternatively 'timevar1' and 'timevar2'
            if name not in rea_object.get_param_states().keys() or rea_object.get_param_states()[name] != 'timevar1':
                new_state = 'timevar1'
            else:
                new_state = 'timevar2'

            def schedule_futureloop_update(name, value, new_state, update_freq):
                rea_object.get_param_states()[name] = new_state
                self.reaproject.set_param_futureloop(rea_object, name, value, new_state, update_freq)
            # beat=None means schedule for the next bar
            self._clock.schedule(schedule_futureloop_update, beat=None, args=[name, value, new_state, update_freq])
        else:
            # to switch back to non varying value use the state normal to make the recursion loop stop
            def schedule_value_update(rea_object, name, value):
                rea_object.get_param_states()[name] = 'normal'
                self.reaproject.add_param_update(rea_object, name, float(value))
            # beat=None means schedule for the next bar
            self._clock.schedule(schedule_value_update, beat=None, args=[rea_object, name, value])

    def get_smart_param(self, full_name):
        # rea_object can point to a fx or a track (self) -> (when param is vol or pan)
        rea_object, name, _ = self.get_reaper_object_and_param_name(full_name)
        if rea_object is None or name is None:
            return
        return getattr(rea_object, name)





class ReaFX(object):

    def __init__(self, fx, name):
        self.fx = fx
        self.name = name
        self.param_name_id_dict = {}
        self.param_states = {}
        for id, param in enumerate(fx.params):
            snake_name = make_snake_name(param.name)
            self.param_name_id_dict[snake_name] = id

    # def get_params(self):
    #     result = {}
    #     for param_name, param in self.params.items():
    #         result[self.name + "_" + param_name] = param
    #     return result

    def __getattr__(self, name):
        if name in ['fx', 'param_name_id_dict', 'name', 'param_states']:
            return self.__dict__[name]
        else:
            return self.fx.params[self.param_name_id_dict[name]]

    def __setattr__(self, name, value):
        if name in ['fx', 'param_name_id_dict', 'name', 'param_states']:
            super().__setattr__(name, value)
        else:
            self.fx.params[self.param_name_id_dict[name]] = value

    def __repr__(self):
        return "<ReaFX {}>".format(self.name)

    def get_param_states(self):
        return self.param_states
