from typing import Mapping
from FoxDot.lib.TimeVar import TimeVar
from FoxDot.lib.Scale import Scale
from FoxDot.lib.Midi import MidiOut
from FoxDot.lib.Patterns import Pattern
from time import sleep
import live




def run_now(f):
    f()
    return f

# This is not realy a decorator, more a currying mechanism using the decorator syntax
# Cf: https://www.geeksforgeeks.org/currying-function-in-python/ and https://www.saltycrane.com/blog/2010/03/simple-python-decorator-examples/
def later_clockless(clock):
    def later_clocked(future_dur):
        def later_decorator(f):
            clock.future(future_dur, f)
            return f
        return later_decorator
    return later_clocked

def normalize_param(param, value):
    if param.maximum == 127:
        return value * 127.0
    else:
        return value * 1.0

def normalize_volume(value):
    """function make volume 1.0 corresponds to gain 0 in ableton (max volume without gain)
    so 1.1 gives the volume some gain"""
    return value * 0.85 if value <= 1.17 else 1.0


    return result

class InstrucFactory:
    def __init__(self, clock, smart_set):
        self._clock = clock
        self._smart_set = smart_set

    def buildInstruc(self, **kwargs):
        return InstrumentFacadeClockless(self._clock, self._smart_set, **kwargs)

reverb_default = {
    "reverb_dw": 0,
    "reverb_hifreq": .89,
    "reverb_lowfreq": .11,
    "reverb_decay": .41,
}

resob_default = {
    "resob_dw": 0,
    "resob_color": .85,
    "resob_gain": .66,
    "resob_width": 1,
}

eq_default = {
    "eq_gainlo": .85,
    "eq_gainmid": .85,
    "eq_gainhi": .85,
    "eq_freqlo": .3,
    "eq_freqhi": .57,
}

delay_default = {
    "delay_vol": 0,
    "delay_time": 0,
    "delay_feedback": .5,
    "delay_pan": .9,
    "delay_dry": 1,
}

config_default = {} | reverb_default | eq_default | resob_default | delay_default




class InstrumentFacadeClockless:

    default_data = [0]
    default_scale = Scale.default
    default_oct = 3
    config_default = config_default

    def __init__(self, clock, smart_set, track_name, channel, grouping=False, oct=None, midi_map=None, config={}, scale=None):
        self._clock = clock
        self._smart_set = smart_set
        self._smart_track = getattr(smart_set, track_name)
        self._channel = channel
        self._grouping = grouping
        self._oct = oct if oct else self.default_oct
        self._config = self.config_default | config
        self._scale = scale if scale is not None else self.default_scale
        if midi_map and isinstance(midi_map, str):
            if midi_map == 'stdrum':
                self._midi_map = self.stdrum_midimap()
            if midi_map == 'threesquare':
                self._midi_map = self.threesquare_midimap()
            if midi_map == 'linear':
                self._midi_map = self.linear_midimap()
        elif midi_map and isinstance(midi_map, Mapping):
            self._midi_map = self.threesquare_midimap() | midi_map # overwrite default midi_map with provided map
        else:
            self._midi_map = self.linear_midimap()

    def linear_midimap(self):
        lowcase = list(range(97,123))
        upcase = list(range(65,91))
        base_midi_map = {'default': 2, ' ': -1}
        for i in range(52):
            if i % 2 == 0:
                base_midi_map[chr(lowcase[i//2])] = i
            else:
                base_midi_map[chr(upcase[i//2])] = i
        return base_midi_map

    def threesquare_midimap(self):
        lowcase = list(range(97,123))
        upcase = list(range(65,91))
        base_midi_map = {'default': 2, ' ': -1}
        for i in range(16):
            base_midi_map[chr(lowcase[i])] = i
        for i in range(16):
            base_midi_map[chr(upcase[i])] = i+16
        for i in range(10):
            k = i + 16
            j = i + 32
            base_midi_map[chr(lowcase[k])] = j
            base_midi_map[chr(upcase[k])] = j+10
        return base_midi_map

    def stdrum_midimap(self):
        lowcase = list(range(97,123))
        upcase = list(range(65,91))
        base_midi_map = {
            'default': 2,
            ' ': -100,
            'x': 0,
            'r': 1,
            'o': 2,
            'c': 3,
            'w': 4,
            'T': 5,
            'H': 6,
            't': 7,
            's': 8,
            'm': 9,
            '=': 10,
            '-': 11,
            'p': 12,
            '*': 13,
            'h': 14,
            'b': 14,
        }

        return base_midi_map


    def _split_param_name(self, name):
        if "_" in name:
            splitted = name.split('_')
            device_name = splitted[0]
            param_name = '_'.join(splitted[1:])
            return device_name, param_name
        else:
            raise KeyError("Parameter name not splittable by '_': " + name)


    def param_exists_in_live(self, smart_track, full_name):
        device_name, param_name = self._split_param_name(full_name)
        if device_name in smart_track.smart_devices.keys():
            smart_device = smart_track.smart_devices[device_name]
            if param_name in smart_device.param_ids.keys():
                return True
        raise KeyError("Parameter doesn't exist: " + full_name)
        return False

    def apply_live_params(self, smart_track, param_dict, remaining_param_dict={}):
        for param, value in param_dict.items():
            if param == "pan":
                smart_track.pan = value
            elif param == "vol":
                smart_track.vol = value
            elif "_" in param and self.param_exists_in_live(smart_track, param):
                device_name, param_name = self._split_param_name(param)
                device = getattr(smart_track, device_name)
                setattr(device, param_name, value)
            else:
                remaining_param_dict[param] = value
        


    def out(self, *args, channel=None, oct=None, scale=None, midi_map=None, dur=1, sus=None, **kwargs):
        midi_map = midi_map if midi_map else self._midi_map
        channel = channel if channel else self._channel
        channel_suffix = "_" + str(channel)
        oct = oct if oct else self._oct
        scale = scale if scale is not None else self._scale
        remaining_kwargs = {}
        sus = Pattern(sus) if sus else Pattern(dur)-0.03 # to avoid midi event collision between start and end note (which prevent the instrument from playing)

        params = self._config | kwargs # overwrite base config with runtime arguments

        if self._grouping: # handle per instrument parameters
            group_subtracks = getattr(self._smart_set, channel_suffix).get_pylive_track().tracks # get the group named like "_6" for the channel then its subtracks
            group_track_names = [track.name[:-len(channel_suffix)] for track in group_subtracks] # get the names and remove the _6 like channel suffix from the names
            for track_name in group_track_names:
                track_params = {key.replace(track_name+"_", ""):value for (key,value) in params.items() if track_name in key.split("_")}
                subtrack = getattr(self._smart_set, track_name+channel_suffix) # get the corresponding smart track
                self.apply_live_params(subtrack, track_params)
                for key in track_params.keys(): # remove per instrument params
                    del params[track_name+"_"+key]

        remaining_param_dict = {}
        self.apply_live_params(self._smart_track, params, remaining_param_dict)
        
                
        return MidiOut(
            midi_map = midi_map,
            channel = self._channel-1,
            oct = oct,
            scale = scale,
            dur = dur,
            sus = sus,
            *args,
            **remaining_param_dict,
        )


class SmartSet(object):

    def __init__(self, clock, set):
        self._clock = clock
        self.__set = set
        self.__tracks = set.tracks
        self.__smart_tracks = {}
        self.__track_names = {}
        self.__track_ids = {}
        for id, track in enumerate(self.__tracks):
            simple_name = track.name.lower().replace(' ','_').replace('/','_')
            self.__track_names[id] = simple_name
            self.__track_ids[simple_name] = id
            self.__smart_tracks[simple_name] = SmartTrack(self._clock, self.__tracks[self.__track_ids[simple_name]])

    def __getattr__(self, name):
        dict_name = '_SmartSet' + name
        if dict_name in self.__dict__.keys():
            return self.__dict__[dict_name]
        else:
            return self.__smart_tracks[name]

    @property
    def vol(self):
        return self.__set.get_master_volume()
    @vol.setter
    def vol(self, value):
        # TODO make this setter TimeVar ready like for smart tracks
        self.__set.set_master_volume(normalize_volume(value))

    @property
    def pan(self):
        return self.__set.get_master_pan()
    @pan.setter
    def pan(self, value):
        self.__set.set_master_pan(value)

class SmartTrack(object):

    def __init__(self, clock, track):
        self._clock = clock
        self.__track = track
        self.__devices = track.devices
        self.__smart_devices = {}
        self.__device_names = {}
        self.__device_ids = {}
        self.__vol_state = 'normal'
        self.__pan_state = 'normal'
        for id, device in enumerate(self.__devices):
            simple_name = device.name.lower().replace(' ','_').replace('/','_')
            self.__device_names[id] = simple_name
            self.__device_ids[simple_name] = id
            self.__smart_devices[simple_name] = SmartDevice(self._clock, self.__devices[self.__device_ids[simple_name]])

    def __getattr__(self, name):
        dict_name = '_SmartTrack' + name
        if dict_name in self.__dict__.keys():
            return self.__dict__[dict_name]
        else:
            return self.__smart_devices[name]

    def get_pylive_track(self):
        return self.__track

    @property
    def device_ids(self):
        return self.__device_ids

    @property
    def devices(self):
        return self.__devices

    @property
    def smart_devices(self):
        return self.__smart_devices

    def __set_vol(self, value, update_freq = 0.05):
        if isinstance(value, TimeVar):
            # to update a time varying param and tell the preceding recursion loop to stop
            # we switch between two timevar state old and new alternatively 'timevar1' and 'timevar2'
            new_state = 'timevar1' if self.__vol_state != 'timevar1' else 'timevar2'
            self.__vol_state = new_state
            self.__set_vol_futureloop(value, new_state, update_freq)
            def schedule_futureloop_update(value, new_state, update_freq):
                self.__vol_state = new_state
                self.__set_vol_futureloop(value, new_state, update_freq)
            self._clock.schedule(schedule_futureloop_update, beat=None, args=[value, new_state, update_freq]) #beat=None means schedule for the next bar
        else:
            # to switch back to non varying value use the state normal to make the recursion loop stop
            def schedule_value_update(value):
                self.__vol_state = 'normal'
                self.__track.volume = normalize_volume(value)
            self._clock.schedule(schedule_value_update, beat=None, args=[value]) #beat=None means schedule for the next bar

    def __set_vol_futureloop(self, value, state, update_freq = 0.05):
        if self.__vol_state == state:
            self.__track.volume = normalize_volume(float(value))
            self._clock.future(update_freq, self.__set_vol_futureloop, args=[value, state], kwargs={"update_freq": update_freq})

    def __set_pan(self, value, update_freq = 0.05):
        if isinstance(value, TimeVar):
            new_state = 'timevar1' if self.__pan_state != 'timevar1' else 'timevar2'
            def schedule_futureloop_update(value, new_state, update_freq):
                self.__pan_state = new_state
                self.__set_pan_futureloop(value, new_state, update_freq)
            self._clock.schedule(schedule_futureloop_update, beat=None, args=[value, new_state, update_freq]) #beat=None means schedule for the next bar
        else:
            def schedule_value_update(value):
                self.__pan_state = 'normal'
                self.__track.pan = value
            self._clock.schedule(schedule_value_update, beat=None, args=[value]) #beat=None means schedule for the next bar

    def __set_pan_futureloop(self, value, state, update_freq = 0.05):
        if self.__pan_state == state:
            self.__track.pan = float(value)
            self._clock.future(update_freq, self.__set_pan_futureloop, args=[value, state], kwargs={"update_freq": update_freq})

    @property
    def vol(self):
        return self.__track.volume
    @vol.setter
    def vol(self, value):
        self.__set_vol(value)

    @property
    def pan(self):
        return self.__track.pan
    @pan.setter
    def pan(self, value):
        self.__set_pan(value)

class SmartDevice(object):
    
    def __init__(self, clock, device):
        self._clock = clock
        self.__device = device
        self.__params = device.parameters
        self.__param_names = {}
        self.__param_ids = {}
        self.__param_states = {}
        for id, param in enumerate(self.__params):
            simple_name = param.name.lower().replace(' ','_').replace('/','_')
            if 'macro' not in simple_name:
                self.__param_names[id] = simple_name
                self.__param_ids[simple_name] = id

    def __getattr__(self, name):
        dict_name = '_SmartDevice' + name
        if dict_name in self.__dict__.keys():
            return self.__dict__[dict_name]
        elif name == 'params':
            return [name for name in self.__param_ids.keys()]
        else:
            return self.__params[self.__param_ids[name]].value

    @property
    def param_ids(self):
        return self.__param_ids

    @property
    def params(self):
        return self.__params

    def __setattr__(self, name, value):
        if name in ['_SmartDevice__device', '_SmartDevice__params', '_SmartDevice__param_names',
                    '_SmartDevice__param_ids', '_SmartDevice__param_states', '_clock']:
            super().__setattr__(name, value)
        else:
            # param = self.__params[self.__param_ids[name]]
            # param.value = normalize_param(param, value)
            self.__set_param(name, value)
        # else:
        #     raise AttributeError("Param value not between 0.0 and 1.0.")

    def __set_param(self, name, value, update_freq = 0.05):
        param = self.__params[self.__param_ids[name]]
        if isinstance(value, TimeVar):
            # to update a time varying param and tell the preceding recursion loop to stop
            # we switch between two timevar state old and new alternatively 'timevar1' and 'timevar2'
            if name not in self.__param_states.keys() or self.__param_states[name] != 'timevar1':
                new_state = 'timevar1'
            else:
                new_state = 'timevar2'
            def schedule_futureloop_update(name, value, new_state, update_freq):
                self.__param_states[name] = new_state
                self.__set_param_futureloop(name, value, new_state, update_freq)
            self._clock.schedule(schedule_futureloop_update, beat=None, args=[name, value, new_state, update_freq]) #beat=None means schedule for the next bar
        else:
            # to switch back to non varying value use the state normal to make the recursion loop stop
            def schedule_value_update(param, value):
                self.__param_states[name] = 'normal'
                param.value = normalize_param(param, value)
            self._clock.schedule(schedule_value_update, beat=None, args=[param, value]) #beat=None means schedule for the next bar

    def __set_param_futureloop(self, name, value, state, update_freq = 0.05):
        param = self.__params[self.__param_ids[name]]
        if self.__param_states[name] == state:
            param.value = normalize_param(param, float(value))
            self._clock.future(update_freq, self.__set_param_futureloop, args=[name, value, state], kwargs={"update_freq": update_freq})



    # def __iter__(self):
    #     for name in self.__slots__:
    #         yield getattr(self, name)

    # def __repr__(self):
    #     values = ', '.join('{}={!r}'.format(*i) for i
    #     in zip(self.__slots__, self))
    #     return '{}({})'.format(self.__class__.__name__, values)

    # cls_attrs = dict(__slots__ = field_names,
    #                 __init__ = __init__,
    #                 __iter__ = __iter__,
    #                 __repr__ = __repr__)

    # return type(cls_name, (object,), cls_attrs)

