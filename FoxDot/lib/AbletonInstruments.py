from . import Player, MidiOut, linvar, Scale
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

    def __init__(self, channel, oct, clock):
        self.midi_channel = channel - 1
        self.clock = clock
        # self.setlive = live.Set()
        # self.setlive.scan(scan_clip_names = True, scan_devices = True)
        # self.track_number = channel - 1
        # self.param_modes = [ 'normal' for i in range(20) ]
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

    # def set_param(self, param_num, value, update_freq = 0.1):
    #     if isinstance(value, linvar):
    #         self.param_modes[param_num] = 'linvar'
    #         self.set_param_futureloop(param_num, value, update_freq)
    #     else:
    #         self.param_modes[param_num] = 'normal'
    #         self.params[param_num].value = normalize_param(self.params[param_num], value)
    #
    #
    # def set_param_futureloop(self, param_num, value, update_freq = 0.1):
    #     if self.param_modes[param_num] == 'linvar':
    #         self.params[param_num].value = normalize_param(self.params[param_num], value)
    #         self.clock.future(update_freq, self.set_param_futureloop, args=[param_num, value], kwargs={"update_freq": update_freq})
    #
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
