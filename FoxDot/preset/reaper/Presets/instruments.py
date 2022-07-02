from .effects import *
from FoxDot import var, sinvar, linvar, expvar, Scale
from functools import partial

# marimba_default = presets["marimba_default"] = {
#  'marimba_on': False,
# }

# vibra_default = presets["vibra_default"] = {
#  'vibra_on': False,
# }


kicker_default = presets["kicker_default"] = {
    'scale': Scale.chromatic,
    'oct': 3,
    'root': 0,
}

presets["crazykit2_default"] = presets["crazykit_default"] = {
    'scale': Scale.major,
    'oct': 3,
    'root': 0,
    'midi_map': "linear",
    # | {
    #     "/": 53,
    #     "-": 54,
    #     "=": 54,
    #     "*": 54,
    #     "%": 54,
    #     "$": 54,
    #     "#": 54,
    #     "&": 54,
    #     "&": 54,
    # }
}
