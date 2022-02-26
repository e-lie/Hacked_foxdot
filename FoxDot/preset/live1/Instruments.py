
from FoxDot.lib.Extensions.Live import arm_all, live_set, smart_set, AbletonInstrumentFactory
from .UtilityFunctions import rndp

from .Presets import presets
from FoxDot import Clock, Scale

arm_all(live_set)

Clock.midi_nudge = 0

ab = AbletonInstrumentFactory(presets, smart_set)

instrucs = ab.instruments_to_instanciate()

for key, value in instrucs.items():
    globals()[key] = value


# smart_set.set_send_ids({
#     "sreverb": 0,
#     "ssc": 1,
#     "sgate": 2,
#     "swh": 3,
#     "swiden": 4,
# })
#
# mixer = ab.create_instruc(track_name="mixer", midi_channel=-1)
#
# sends = ab.create_instruc(track_name="sends", midi_channel=-1, set_defaults=False)
#
#
# metronome = ab.create_instruc(
#     track_name="metronome",
#     midi_channel=16,
#     set_defaults=False,
#     scale=Scale.chromatic,
#     oct=3,
#     config={"root": 0},
#     midi_map="stdrum",
# )
#
# # Channel 1
#
# kit808 = ab.create_instruc(
#     track_name="kit808",
#     midi_channel=1,
#     scale=Scale.chromatic,
#     oct=3,
#     config={"root": 0},
#     midi_map="stdrum",
#     dur=1 / 2,
# )
#
# kicker = ab.create_instruc(
#     track_name="kicker",
#     midi_channel=1,
#     config={"root": 0},
#     scale=Scale.chromatic,
#     oct=1.6,
#     midi_map="threesquare",
#     dur=1,
# )
#
# kitdatai = ab.create_instruc(
#     track_name="kitdatai",
#     midi_channel=1,
#     config={"root": 0},
#     scale=Scale.chromatic,
#     oct=4.4,
#     midi_map="stdrum",
#     dur=1 / 2,
# )
#
# # Channel 2
#
# kitcuba = ab.create_instruc(
#     track_name="_2",
#     midi_channel=2,
#     oct=3,
#     dur=1 / 2,
#     midi_map="stdrum",
#     config={
#         "root": 0,
#         "kitcuba_vol": 1,
#         "jazzkit_vol": 0,
#         "reaktorkit_vol": 0,
#         "harshkit_vol": 0,
#     },
#     scale=Scale.chromatic,
# )
#
# jazzkit = ab.create_instruc(
#     track_name="_2",
#     midi_channel=2,
#     oct=3,
#     dur=1 / 2,
#     midi_map="stdrum",
#     config={
#         "root": 0,
#         "kitcuba_vol": 0,
#         "jazzkit_vol": 1,
#         "reaktorkit_vol": 0,
#         "harshkit_vol": 0,
#     },
#     scale=Scale.chromatic,
# )
#
# reaktorkit = ab.create_instruc(
#     track_name="_2",
#     midi_channel=2,
#     oct=3,
#     dur=1 / 2,
#     midi_map="stdrum",
#     config={
#         "root": 0,
#         "kitcuba_vol": 0,
#         "jazzkit_vol": 0,
#         "reaktorkit_vol": 1,
#         "harshkit_vol": 0,
#     },
#     scale=Scale.chromatic,
# )
#
# harshkit = ab.create_instruc(
#     track_name="_2",
#     midi_channel=2,
#     oct=3,
#     dur=1 / 2,
#     midi_map="stdrum",
#     config={
#         "root": 0,
#         "kitcuba_vol": 0,
#         "jazzkit_vol": 0,
#         "reaktorkit_vol": 0,
#         "harshkit_vol": 1,
#     },
#     scale=Scale.chromatic,
# )
#
# # Channel 6
#
# crubass = ab.create_instruc(
#     track_name="_6",
#     midi_channel=6,
#     oct=3,
#     # sus=1/2, #the sustain bug disappeared
#     config={
#         "ubass_vol": 0,
#         "crubass_vol": 1,
#         "tb303_vol": 0,
#     }
#     | rndp(crubassp, 12),
# )
#
#
# tb303 = ab.create_instruc(
#     track_name="_6",
#     midi_channel=6,
#     oct=4,
#     # sus=1/2,
#     config={
#         "ubass_vol": 0,
#         "crubass_vol": 0,
#         "tb303_vol": 0.9,
#     },
# )
#
# ubass = ab.create_instruc(
#     track_name="_6",
#     midi_channel=6,
#     oct=4,
#     config={
#         "ubass_vol": 0.9,
#         "crubass_vol": 0,
#         "tb303_vol": 0,
#     },
# )
#
# # Channel 7
#
# crubass_2 = ab.create_instruc(
#     track_name="_7",
#     midi_channel=7,
#     oct=4,
#     config={
#         "ubass_vol": 0,
#         "crubass_vol": 1,
#         "tb303_vol": 0,
#     }
#     | rndp(crubassp, 12),
# )
#
# tb303_2 = ab.create_instruc(
#     track_name="_7",
#     midi_channel=7,
#     oct=4,
#     config={
#         "ubass_vol": 0,
#         "crubass_vol": 0,
#         "tb303_vol": 0.9,
#     },
# )
#
# # Channel 8
#
# piano = ab.create_instruc(
#     track_name="_8",
#     midi_channel=8,
#     oct=5,
#     config={
#         "piano_vol": 1,
#         "danceorg_vol": 0,
#     },
# )
#
# danceorg = ab.create_instruc(
#     track_name="_8",
#     midi_channel=8,
#     oct=5,
#     config={
#         "piano_vol": 0,
#         "danceorg_vol": 1,
#     },
# )
#
# kora = ab.create_instruc(
#     track_name="_4",
#     midi_channel=4,
#     oct=5,
#     config={
#         "kora_vol": 1,
#     },
# )
#
# strings = ab.create_instruc(
#     track_name="_9",
#     midi_channel=9,
#     oct=5,
#     config={
#         "strings_vol": 1,
#         "owstr_vol": 0,
#     },
# )
#
# owstr = ab.create_instruc(
#     track_name="_9",
#     midi_channel=9,
#     oct=5,
#     config={
#         "strings_vol": 0,
#         "owstr_vol": 1,
#     },
# )
#
# balafon = ab.create_instruc(
#     track_name="_10",
#     midi_channel=10,
#     oct=5,
#     config={
#         "balafon_vol": 1,
#         "bells_vol": 0,
#     },
# )
#
# bells = ab.create_instruc(
#     track_name="_10",
#     midi_channel=10,
#     oct=5,
#     config={
#         "balafon_vol": 0,
#         "bells_vol": 1,
#     },
# )
