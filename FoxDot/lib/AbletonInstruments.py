from . import Player, MidiOut, linvar
import live


class Instruc:
    default_amplitude = 1
    default_pitch = [0]
    default_duration = 1
    default_sustain = default_duration - 0.01

    def __init__(self, channel, oct, clock):
        self.setlive = live.Set()
        self.setlive.scan(scan_clip_names = True, scan_devices = True)
        self.player = Player()
        self.clock = clock
        self.midi_channel = channel - 1
        self.track_number = channel - 1
        self.param_modes = [ 'normal' for i in range(20) ]
        self.track = self.setlive.tracks[self.track_number]
        self.mdevice = self.setlive.tracks[self.track_number].devices[0] if self.setlive.tracks[self.track_number].devices else None
        self.params = self.setlive.tracks[self.track_number].devices[0].parameters
        self.oct = oct
        self._amp = self.default_amplitude
        self._dur = self.default_duration
        self._pitch = self.default_pitch
        self._sus = self.default_sustain


    def setup(self, pitch=-1, dur=-1, sus=-1, amp=-1, oct=-1, no_play=False):
        self.mdevice.parameters[0] = True
        self.oct = oct if oct != -1 else self.oct
        self._amp = amp if amp != -1 else self._amp
        self._dur = dur if dur != -1 else self._dur
        self._pitch = pitch if pitch != -1 else self._pitch
        self._sus = sus if sus != -1 else self._sus
        if not no_play:
            self.play()
        return self

    def later(self, future_dur, pitch=-1, dur=-1, sus=-1, amp=-1, oct=-1):
        self.setup(pitch, dur=dur, sus=sus, amp=amp, oct=oct, no_play=True)
        self.clock.future(future_dur, self.play)

    def __del__(self):
        self.player.stop()

    def play(self):
        self.player >> MidiOut(
            self._pitch,
            channel=self.midi_channel,
            dur=self._dur,
            sus=self._sus,
            amp=self._amp,
            oct=self.oct
        )

    def set_param(self, param_num, value, update_freq = 0.5):
        if isinstance(value, linvar):
            self.param_modes[param_num] = 'linvar'
            self.set_param_futureloop(param_num, value, update_freq)
        else:
            self.param_modes[param_num] = 'normal'
            self.params[param_num].value = int(value)


    def set_param_futureloop(self, param_num, value, update_freq = 0.5):
        if self.param_modes[param_num] == 'linvar':
            self.params[param_num].value = int(value)
            self.clock.future(update_freq, self.set_param_futureloop, args=[param_num, value], kwargs={"update_freq": update_freq})

    def stop(self, dur=None):
        if dur:
            self.clock.future(dur, self.stop)
        else:
            self.player.stop()

    @property
    def amp(self):
        return self._amp
    @amp.setter
    def amp(self, amplitude):
        self._amp=amplitude
        self.play()

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


    def display_set(self):
        for i, track in enumerate(self.setlive.tracks):
            print("\n" + str(i) + " - " + str(track))
            print("===========================")
            for j, device in enumerate(track.devices):
                print(str(j) + " - " + str(device))
                print("------------------------------------")
                for k, parameter in enumerate(device.parameters):
                    print(str(k) + " - " + str(parameter))
