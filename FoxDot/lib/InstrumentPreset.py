import live

from .Scale import Scale
from . import Clock

from . import SmartSet, InstrucFactory

liveset = live.Set()
liveset.scan(scan_clip_names = True, scan_devices = True)
ab = SmartSet(Clock, liveset)
Instruc  = InstrucFactory(Clock,ab).buildInstruc

mixer = Instruc(track_name="mixer", channel=-1, scale=Scale.chromatic, oct=3, midi_map="stdrum").out

def arm_all():
    for track in liveset.tracks:
        track.arm=1

arm_all()

# Channel 2

kit808 = Instruc(track_name="kit808", channel=1, scale=Scale.chromatic, oct=3, midi_map="stdrum").out
kicker = Instruc(track_name="kicker", channel=1, scale=Scale.chromatic, oct=1.6, midi_map="threesquare").out
kitdatai = Instruc(track_name="kitdatai", channel=1, scale=Scale.chromatic, oct=4.4, midi_map="stdrum").out

# Channel 2

kitcuba =  Instruc(track_name="channel_2",
                    channel=2,
                    grouping=True,
                    oct=3,
                    midi_map="stdrum",
                    config={
                        "kitcuba_vol": 1,
                        "jazzkit_vol": 0,
                        "reaktorkit_vol": 0,
                        "harshkit_vol": 0,
                    },
                    scale=Scale.chromatic).out

jazzkit =  Instruc(track_name="channel_2",
                    channel=2,
                    grouping=True,
                    oct=3,
                    midi_map="stdrum",
                    config={
                        "kitcuba_vol": 0,
                        "jazzkit_vol": 1,
                        "reaktorkit_vol": 0,
                        "harshkit_vol": 0,
                    },
                    scale=Scale.chromatic).out

reaktorkit =  Instruc(track_name="channel_2",
                    channel=2,
                    grouping=True,
                    oct=3,
                    midi_map="stdrum",
                    config={
                        "kitcuba_vol": 0,
                        "jazzkit_vol": 0,
                        "reaktorkit_vol": 1,
                        "harshkit_vol": 0,
                    },
                    scale=Scale.chromatic).out

harshkit =  Instruc(track_name="channel_2",
                    channel=2,
                    grouping=True,
                    oct=3,
                    midi_map="stdrum",
                    config={
                        "kitcuba_vol": 0,
                        "jazzkit_vol": 0,
                        "reaktorkit_vol": 0,
                        "harshkit_vol": 1,
                    },
                    scale=Scale.chromatic).out

# Channel 6

crubass =  Instruc(track_name="channel_6",
                    channel=6,
                    grouping=True,
                    oct=4,
                    config={
                        "ubass_vol": .9,
                        "crubass_vol": .8,
                        "tb303_vol": 0,
                    },
                    scale=Scale.minor).out

tb303 =  Instruc(track_name="channel_6",
                 channel=6,
                 grouping=True,
                 oct=4,
                 config={
                     "ubass_vol": 0,
                     "crubass_vol": 0,
                     "tb303_vol": .9,
                 },
                 scale=Scale.minor).out

ubass =  Instruc(track_name="channel_6",
                 channel=6,
                 grouping=True,
                 oct=4,
                 config={
                     "ubass_vol": .9,
                     "crubass_vol": 0,
                     "tb303_vol": 0,
                 },
                 scale=Scale.minor).out

# Channel 7

crubass_2 =  Instruc(track_name="channel_7",
                    channel=7,
                    grouping=True,
                    oct=4,
                    config={
                        "ubass_vol": .9,
                        "crubass_vol": .8,
                        "tb303_vol": 0,
                    },
                    scale=Scale.minor).out

tb303_2 =  Instruc(track_name="channel_7",
                 channel=7,
                 grouping=True,
                 oct=4,
                 config={
                     "ubass_vol": 0,
                     "crubass_vol": 0,
                     "tb303_vol": .9,
                 },
                 scale=Scale.minor).out

# Channel 8

piano =  Instruc(track_name="channel_8",
                 channel=8,
                 grouping=True,
                 oct=5,
                 config={
                     "piano_vol": 1,
                     "danceorg_vol": 0,
                 },
                 scale=Scale.minor).out

danceorg =  Instruc(track_name="channel_8",
                 channel=8,
                 grouping=True,
                 oct=5,
                 config={
                     "piano_vol": 0,
                     "danceorg_vol": 1,
                 },
                 scale=Scale.minor).out

kora =  Instruc(track_name="channel_4",
                 channel=4,
                 grouping=True,
                 oct=5,
                 config={
                     "kora_vol": 1,
                 },
                 scale=Scale.major).out

strings =  Instruc(track_name="channel_9",
                 channel=9,
                 grouping=True,
                 oct=5,
                 config={
                     "strings_vol": 1,
                     "owstr_vol": 0,
                 },
                 scale=Scale.major).out

owstr =  Instruc(track_name="channel_9",
                 channel=9,
                 grouping=True,
                 oct=5,
                 config={
                     "strings_vol": 0,
                     "owstr_vol": 0,
                 },
                 scale=Scale.major).out

balafon =  Instruc(track_name="channel_10",
                 channel=10,
                 grouping=True,
                 oct=5,
                 config={
                     "balafon_vol": 1,
                     "bells_vol": 0,
                 },
                 scale=Scale.major).out

bells =  Instruc(track_name="channel_10",
                 channel=10,
                 grouping=True,
                 oct=5,
                 config={
                     "balafon_vol": 0,
                     "bells_vol": 1,
                 },
                 scale=Scale.major).out
