from functools import partial

import live

from .Scale import Scale
from . import Clock

from . import SmartSet, InstrucFactory, MusicStateMachine, delay_clockless


## Definition / partials

delay = partial(delay_clockless, Clock)
set = live.Set()
set.scan(scan_clip_names = True, scan_devices = True)
ab = SmartSet(Clock, set)
Instruc  = InstrucFactory(Clock,ab).buildInstruc

msm = MusicStateMachine


# mixer = Instruc(smart_track=ab.mixer, midi_channel=-1, scale=Scale.chromatic, oct=3, midi_map="stdrum").out

# kitcuba = Instruc(smart_track=ab.kitcuba, midi_channel=1, scale=Scale.chromatic, oct=3, midi_map="stdrum").out
# kitdnb = Instruc(smart_track=ab.kitcuba, midi_channel=2, scale=Scale.chromatic, oct=3, midi_map="stdrum").out
# kit808 = Instruc(smart_track=ab.kitdatai, midi_channel=3, scale=Scale.chromatic, oct=3, midi_map="stdrum").out
# kicker = Instruc(smart_track=ab.kicker, midi_channel=4, scale=Scale.chromatic, oct=3).out
# kitdatai = Instruc(smart_track=ab.kitdatai, midi_channel=5, scale=Scale.chromatic, oct=3, midi_map="stdrum").out

# ubass = Instruc(smart_track=ab.ubass, midi_channel=6, oct=4, scale=Scale.minor).out
# tb303 = Instruc(smart_track=ab.tb303, midi_channel=7, oct=4, scale=Scale.minor).out
# crubass = Instruc(smart_track=ab.crubass, midi_channel=8, oct=4, scale=Scale.minor).out

# strings = Instruc(smart_track=ab.strings, midi_channel=9, oct=5, scale=Scale.minor).out
# owstrings = Instruc(smart_track=ab.owstrings, midi_channel=10, oct=5, scale=Scale.minor).out

# balafon = Instruc(smart_track=ab.balafon, midi_channel=11, oct=6, scale=Scale.minor).out
# bells = Instruc(smart_track=ab.bells, midi_channel=12, oct=6, scale=Scale.minor).out

# kora = Instruc(smart_track=ab.bells, midi_channel=13, oct=6, scale=Scale.minor).out

balafon = Instruc(track_name="balafon", midi_channel=11, oct=5, scale=Scale.minor).out