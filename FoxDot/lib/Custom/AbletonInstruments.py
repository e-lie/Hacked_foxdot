from FoxDot.lib.TimeVar import TimeVar
from .. import Player, MidiOut, linvar, Scale, Clock
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

def interpolate(start, end, step=5, go_back=True):
    assert len(start) == len(end)
    diffs = []
    result = []
    for i in range(len(start)):
        diffs += [start[i] - end[i]]
    base_pattern = start
    for j in range(step):
        new_pattern = [ e - diffs[k]/(step+1) for k, e in enumerate(base_pattern)]
        result.append(new_pattern)
        base_pattern = new_pattern
    if not go_back:
        result = [start] + result + [end]
    else:
        result = [start] + result + [end] + result[::-1] # result except last elem + end + reversed result
    return result



class MidiFacade:

    default_data = [0]
    default_scale = Scale.chromatic
    default_midi_channel = 1
    default_oct = 3

    def __init__(self, midi_channel=None, oct=None, scale=None, midi_map=None):
        self._midi_channel = midi_channel if midi_channel else self.default_midi_channel
        self._oct = oct if oct else self.default_oct
        self._scale = scale if scale else self.default_scale
        self._midi_map = midi_map if midi_map else self.default_midimap()

    # def init(self, data=-1, dur=-1, sus=-1, amp=-1, oct=-1, scale=-1, midi_map=-1):
    #     # self.mdevice.parameters[0] = True
    #     self.oct = oct if oct != -1 else self.oct
    #     self._amp = amp if amp != -1 else self.default_amplitude
    #     self._dur = dur if dur != -1 else self.default_duration
    #     self.data = data if data != -1 else self.default_data
    #     self._sus = sus if sus != -1 else self.default_sustain
    #     self._scale = scale if scale != -1 else self.default_scale
    #     self._midi_map = midi_map if midi_map != -1 else None
    #     return self.out()

    # def setup(self, data=-1, dur=-1, sus=-1, amp=-1, oct=-1, scale=-1):
    #     # self.mdevice.parameters[0] = True
    #     self.oct = oct if oct != -1 else self.oct
    #     self._amp = amp if amp != -1 else self._amp
    #     self._dur = dur if dur != -1 else self._dur
    #     self._data = data if data != -1 else self._data
    #     self._sus = sus if sus != -1 else self._sus
    #     self._scale = scale if scale != -1 else self._scale
    #     return self.out()

    def default_midimap(self):
        lowcase = list(range(97,123))
        upcase = list(range(65,91))
        base_midi_map = {'default': 2, ' ': -1}
        for i in range(52):
            if i % 2 == 0:
                base_midi_map[chr(lowcase[i//2])] = i
            else:
                base_midi_map[chr(upcase[i//2])] = i
        return base_midi_map

    def out(self, *args, midi_channel=None, oct=None, scale=None, midi_map=None, **kwargs):
        midi_map = midi_map if midi_map else self._midi_map
        midi_channel = midi_channel if midi_channel else self._midi_channel
        oct = oct if oct else self._oct
        scale = scale if scale else self._scale
        return MidiOut(
            midi_map = midi_map,
            midi_channel = midi_channel,
            oct = oct,
            scale = scale,
            *args,
            **kwargs,
        )


class SmartSet(object):

    def __init__(self, set):
        self.__set = set
        self.__tracks = set.tracks
        self.__smart_tracks = {}
        self.__track_names = {}
        self.__track_ids = {}
        for id, track in enumerate(self.__tracks):
            simple_name = track.name.lower().replace(' ','_').replace('/','_')
            self.__track_names[id] = simple_name
            self.__track_ids[simple_name] = id
            self.__smart_tracks[simple_name] = SmartTrack(self.__tracks[self.__track_ids[simple_name]])

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
        self.__set.set_master_volume(value)

    @property
    def pan(self):
        return self.__set.get_master_pan()
    @pan.setter
    def pan(self, value):
        self.__set.set_master_pan(value)

class SmartTrack(object):

    def __init__(self, track):
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
            self.__smart_devices[simple_name] = SmartDevice(self.__devices[self.__device_ids[simple_name]])

    def __getattr__(self, name):
        dict_name = '_SmartTrack' + name
        if dict_name in self.__dict__.keys():
            return self.__dict__[dict_name]
        elif name == 'devices':
            return [name for name in self.__device_ids.keys()]
        else:
            return self.__smart_devices[name]

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
            Clock.schedule(schedule_futureloop_update, beat=None, args=[value, new_state, update_freq]) #beat=None means schedule for the next bar
        else:
            # to switch back to non varying value use the state normal to make the recursion loop stop
            def schedule_value_update(value):
                self.__vol_state = 'normal'
                self.__track.volume = value
            Clock.schedule(schedule_value_update, beat=None, args=[value]) #beat=None means schedule for the next bar

    def __set_vol_futureloop(self, value, state, update_freq = 0.05):
        if self.__vol_state == state:
            self.__track.volume = float(value)
            Clock.future(update_freq, self.__set_vol_futureloop, args=[value, state], kwargs={"update_freq": update_freq})

    def __set_pan(self, value, update_freq = 0.05):
        if isinstance(value, TimeVar):
            new_state = 'timevar1' if self.__pan_state != 'timevar1' else 'timevar2'
            def schedule_futureloop_update(value, new_state, update_freq):
                self.__pan_state = new_state
                self.__set_pan_futureloop(value, new_state, update_freq)
            Clock.schedule(schedule_futureloop_update, beat=None, args=[value, new_state, update_freq]) #beat=None means schedule for the next bar
        else:
            def schedule_value_update(value):
                self.__pan_state = 'normal'
                self.__track.pan = value
            Clock.schedule(schedule_value_update, beat=None, args=[value]) #beat=None means schedule for the next bar

    def __set_pan_futureloop(self, value, state, update_freq = 0.05):
        if self.__pan_state == state:
            self.__track.pan = float(value)
            Clock.future(update_freq, self.__set_pan_futureloop, args=[value, state], kwargs={"update_freq": update_freq})

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
    
    def __init__(self, device):
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

    def __setattr__(self, name, value):
        if name in ['_SmartDevice__device', '_SmartDevice__params', '_SmartDevice__param_names', '_SmartDevice__param_ids', '_SmartDevice__param_states']:
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
            Clock.schedule(schedule_futureloop_update, beat=None, args=[name, value, new_state, update_freq]) #beat=None means schedule for the next bar
        else:
            # to switch back to non varying value use the state normal to make the recursion loop stop
            def schedule_value_update(param, value):
                self.__param_states[name] = 'normal'
                param.value = normalize_param(param, value)
            Clock.schedule(schedule_value_update, beat=None, args=[param, value]) #beat=None means schedule for the next bar

    def __set_param_futureloop(self, name, value, state, update_freq = 0.05):
        param = self.__params[self.__param_ids[name]]
        if self.__param_states[name] == state:
            param.value = normalize_param(param, float(value))
            Clock.future(update_freq, self.__set_param_futureloop, args=[name, value, state], kwargs={"update_freq": update_freq})



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

