from . import Player, MidiOut

class MidiInstrument:
    default_midi_channel = -1
    default_midi_octave = 1
    default_amplitude = 1
    default_duration = 1
    default_sustain = default_duration - 0.01

    def __init__(self):
        self.player = Player()

    def setup(self, pitch, midi_channel=-1, dur=-1, sus=-1, amp=-1, oct=-1):
        self.pitch = pitch
        self.midi_channel = midi_channel if midi_channel != -1 else self.default_midi_channel
        self.oct = oct if oct != -1 else self.default_midi_octave
        self._amp = amp if amp != -1 else self.default_amplitude
        self._dur = dur if dur != -1 else self.default_duration
        self._sus = sus if sus != -1 else self.default_sustain
        self.play()
        return self

    def __del__(self):
        self.player.stop()

    def play(self):
        self.player >> MidiOut(
            self.pitch,
            channel=self.midi_channel,
            dur=self._dur,
            sus=self._sus,
            amp=self._amp,
            oct=self.oct
        )

    def stop(self):
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

class Kit808(MidiInstrument):
    default_midi_channel = 2
    default_midi_octave = 2

class Piano(MidiInstrument):
    default_midi_channel = 4

class Percu(MidiInstrument):
    default_midi_channel = 3
    default_midi_octave = 2
