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
# later = later_dry(Clock) ## to define in during the FoxDot module __init__ after Clock variable definition

# run_later = later_clockless(Clock)

# def set_param_futureloop_clockless(clock):
#     def set_param_futureloop_clocked(param, value, update_freq = 0.1):
#         if param.state == 'linvar':
#             param.value = normalize_param(param, value)
#             clock.future(update_freq, set_param_futureloop_clocked, args=[param, value], kwargs={"update_freq": update_freq})
#     return set_param_futureloop_clocked

# set_param_futureloop = set_param_futureloop_clockless(Clock)

# def set_param(param, value, update_freq = 0.1):
#     if isinstance(value, linvar):
#         param.state = 'linvar'
#         set_param_futureloop(param, value, update_freq)
#     else:
#         param.state = 'normal'
#         param.value = normalize_param(param, value)


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





class Instruc:
    default_amplitude = 1
    default_data = [0]
    default_duration = 1
    default_sustain = default_duration - 0.01
    default_scale = Scale.chromatic

    def __init__(self, channel, oct):
        self.midi_channel = channel - 1
        # self.setlive = live.Set()
        # self.setlive.scan(scan_clip_names = True, scan_devices = True)
        # self.track_number = channel - 1
        # self.param_states = [ 'normal' for i in range(20) ]
        # self.track = self.setlive.tracks[self.track_number]
        # self.mdevice = self.setlive.tracks[self.track_number].devices[0] if self.setlive.tracks[self.track_number].devices else None
        # self.params = self.setlive.tracks[self.track_number].devices[0].parameters
        self.oct = oct
        self._amp = self.default_amplitude
        self._dur = self.default_duration
        self._data = self.default_data
        self._sus = self.default_sustain
        self._scale = self.default_scale
        self._midi_map = None

    def init(self, data=-1, dur=-1, sus=-1, amp=-1, oct=-1, scale=-1, midi_map=-1):
        # self.mdevice.parameters[0] = True
        self.oct = oct if oct != -1 else self.oct
        self._amp = amp if amp != -1 else self.default_amplitude
        self._dur = dur if dur != -1 else self.default_duration
        self.data = data if data != -1 else self.default_data
        self._sus = sus if sus != -1 else self.default_sustain
        self._scale = scale if scale != -1 else self.default_scale
        self._midi_map = midi_map if midi_map != -1 else None
        return self.out()

    def setup(self, data=-1, dur=-1, sus=-1, amp=-1, oct=-1, scale=-1):
        # self.mdevice.parameters[0] = True
        self.oct = oct if oct != -1 else self.oct
        self._amp = amp if amp != -1 else self._amp
        self._dur = dur if dur != -1 else self._dur
        self._data = data if data != -1 else self._data
        self._sus = sus if sus != -1 else self._sus
        self._scale = scale if scale != -1 else self._scale
        return self.out()

    def out(self):
        return MidiOut(
            self._data,
            channel=self.midi_channel,
            dur=self._dur,
            sus=self._sus,
            amp=self._amp,
            oct=self.oct,
            scale=self._scale,
            midi_map=self._midi_map,
        )

    @property
    def amp(self):
        return self._amp
    @amp.setter
    def amp(self, amplitude):
        self._amp=amplitude
        self.play()

    @property
    def data(self):
        return self._amp
    @data.setter
    def data(self, data):
        # if type(data) is str:
        #     print("striiing")
        self._data=data
        # self.play()

    @property
    def dur(self):
        return self._dur
    @dur.setter
    def dur(self, duration):
        self._dur=duration
        if not self.sus or self.sus > self.dur-0.03:
            self._sus=duration - 0.01
        self.play()

    @property
    def sus(self):
        return self._dur
    @sus.setter
    def sus(self, sustain):
        self._sus=min(sustain, self.dur-0.01)
        self.play()


    # def display_set(self):
    #     for i, track in enumerate(self.setlive.tracks):
    #         print("\n" + str(i) + " - " + str(track))
    #         print("===========================")
    #         for j, device in enumerate(track.devices):
    #             print(str(j) + " - " + str(device))
    #             print("------------------------------------")
    #             for k, parameter in enumerate(device.parameters):
    #                 print(str(k) + " - " + str(parameter))
    #
    # def show(self):
    #     for j, device in enumerate(self.setlive.tracks[self.track_number].devices):
    #         print(str(j) + " - " + str(device))
    #         print("------------------------------------")
    #         for k, parameter in enumerate(device.parameters):
    #             print(str(k) + " - " + str(parameter))


# set = live.Set()
# set.scan(scan_clip_names = True, scan_devices = True)
# frenchkit_track = set.tracks[4]
# frenchkit = frenchkit_track.devices[0]
# frenchkit_reso = frenchkit_track.devices[1]
# frenchkit_eq = frenchkit_track.devices[2]
# frenchkit_delay = frenchkit_track.devices[3]
# frenchkit_reverb = frenchkit_track.devices[4]
# frenchkit_reverb_dw = frenchkit_track.devices[4].parameters[1]



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


# class SmartDevice:
#     def __init__(self, device):
#         self.device=device

# class EffectChain:

#     def __init__(self, set_live, track_num, offset=1):
#         self._reso = set_live.tracks[track_num].devices[offset+0]
#         self._eq = set_live.tracks[track_num].devices[offset+1]
#         self._delay = set_live.tracks[track_num].devices[offset+2]
#         self._reverb = set_live.tracks[track_num].devices[offset+3]

#         self._reso_onoff_param = self._reso.parameters[0]
#         self._reso_dw_param = self._reso.parameters[1]
#         self._reso_color_param = self._reso.parameters[2]
#         self._reso_gain_param = self._reso.parameters[3]
#         self._reso_width_param = self._reso.parameters[4]

#         self._eq_onoff_param = self._eq.parameters[0]
#         self._eq_low_param = self._eq.parameters[1]
#         self._eq_mid_param = self._eq.parameters[2]
#         self._eq_high_param = self._eq.parameters[3]
#         self._eq_low_thresh_param = self._eq.parameters[4]
#         self._eq_high_thresh_param = self._eq.parameters[5]

#         self._delay_onoff_param = self._delay.parameters[0]
#         self._delay_vol_param = self._delay.parameters[1]
#         self._delay_time_param = self._delay.parameters[2]
#         self._delay_feedback_param = self._delay.parameters[3]
#         self._delay_pan_param = self._delay.parameters[4]

#         self._reverb_onoff_param = self._reverb.parameters[0]
#         self._reverb_dw_param = self._reverb.parameters[1]
#         self._reverb_high_param = self._reverb.parameters[2]
#         self._reverb_low_param = self._reverb.parameters[3]
#         self._reverb_decay_param = self._reverb.parameters[4]

#     @property
#     def reso(self):
#         return normalize_param(self._reso_dw_param.value
#     @reso.setter
#     def reso(self, value):
#         self._reso_dw_param.value = value

#     @property
#     def eq_low(self):
#         return self._eq_low_param.value
#     @eq_low.setter
#     def eq_low(self, value):
#         self._eq_low_param.value = value

#     @property
#     def eq_mid(self):
#         return self._eq_mid_param.value
#     @eq_mid.setter
#     def eq_mid(self, value):
#         self._eq_mid_param.value = value

#     @property
#     def eq_high(self):
#         return self._eq_high_param.value
#     @eq_high.setter
#     def eq_high(self, value):
#         self._eq_high_param.value = value

#     @property
#     def eq_lth(self):
#         return self._eq_low_thresh_param.value
#     @eq_lth.setter
#     def eq_lth(self, value):
#         self._eq_low_thresh_param.value = value

#     @property
#     def eq_hth(self):
#         return self._eq_high_thresh_param.value
#     @eq_lth.setter
#     def eq_hth(self, value):
#         self._eq_high_thresh_param.value = value

#     @property
#     def lpf(self):
#         return self._eq_low_thresh_param.value
#     @lpf.setter
#     def lpf(self, value):
#         self._eq_low_param.value = 127
#         self._eq_low_thresh_param.value = value

#     @property
#     def hpf(self):
#         return self._eq_high_thresh_param.value
#     @hpf.setter
#     def hpf(self, value):
#         self._eq_high_param.value = 127
#         self._eq_high_thresh_param.value = value

