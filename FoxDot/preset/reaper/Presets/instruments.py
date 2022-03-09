from .effects import *
from FoxDot import var, sinvar, linvar, expvar, Scale

presets["crubass_default"] = {
    "i_wt_pos":.2,
    "i_glide":3,
    "i_intensity":.8,
    "i_cutoff":.1,
    "i_crush":.2,
    "i_delay":.4,
    "i_reso":.3,
    "i_filter":.3,
}

presets["tb303_default"] = {
    "i_decay":.2,
    "i_freq":3,
    "i_reso":.8,
    "i_drive":.1,
    "i_delay":.2,
    "i_dfreq":.4,
}

presets["ubass_default"] = {
    "i_wt_pos":.2,
    "i_drive":3,
    "i_intensity":.8,
    "i_chorus":.1,
    "i_cutoff":.2,
    "i_flt_dec":.4,
    "i_reso":.3,
    "i_dec_time":.3,
}

presets["bells_default"] = {
    "i_bright":.2,
    "i_detune":.2,
    "i_material":.2,
    "i_mod_amount":.2,
    "i_attack":.2,
    "i_decay":.2,
    "i_mod_freq":.2,
    # "i_volume":.2, # keep it 0dB
}

presets["piano_default"] = {
    "i_bright":.2,
    "i_hardness":.2,
    "i_glue":.2,
    "i_reverb":.2,
    "i_attack":.2,
    "i_release":.2,
    "i_tone":.2,
    # "i_volume":.2,
}

presets["danceorg_default"] = {
    "i_bright":.2,
    "i_spike":.2,
    "i_tone":.2,
    "i_space":.2,
    "i_attack":.2,
    "i_release":.2,
    "i_tremolo":.2,
    # "i_volume":.2,
}

presets["danceorg_amb1"] = {
    "i_bright":0,
    "i_spike":0,
    "i_tone":.9,
    "i_space":.7,
    "i_attack":.7,
    "i_release":.8,
    "i_tremolo":0,
    # "i_volume":.2,
}

owstr_default = presets["owstr_default"] = {
 'i_attack': 0.5,
 'i_bright': 0.5,
 'i_reso': 0.5,
 'i_interval': 0.7,
 'i_motion': 0.5,
 #'i_vol': 0.7,
 'i_release': 0.5,
 'i_reverb': 0.5,
}

owstr_1 = presets["owstr_1"] = {
    'i_attack': 0.0,
    'i_bright': sinvar([.3,1], 8),
    'i_filter_res': 0.6575854444128322,
    'i_interval': var([.5,.9,.6],3),
    'i_motion': 0.7007874015748031,
    #'i_vol': 0.7,
    'i_release': 0.1889763779527559,
    'i_reverb_amount': 0.8976377952755905,
}

marimba_default = presets["marimba_default"] = {'i_attack': 0.14960629921259844,
 'i_bright': 0.6062992125984252,
 'i_distortion': 0.31496062992125984,
 'i_overtone': 0.5039370078740157,
 'i_release': 0.5590551181102362,
 'i_reverb': 0.4645669291338583,
 'i_tone': 0.0,
 #'i_volume': 0.8500000360443836
}

kit808_default = presets["kit808_default"] = {
    'dur': .5,
    'oct': 3,
    'root': 0,
    'midi_map': "stdrum",
    'scale': Scale.chromatic
}

crubass_1 = presets["crubass_1"] = {
 'i_crush': 0.19999999699630136,
 'i_cutoff': 0.09999999849815068,
 'i_delay': 0.3999999939926027,
 'i_filter': 0.29999998798520544,
 'i_glide': 0.0,
 'i_intensity': 0.7999999879852054,
 'i_reso': 0.29999998798520544,
 'i_wt_pos': 0.19999999699630136}

kicker_default = presets["kicker_default"] = {
    'scale': Scale.chromatic,
    'oct': 3,
    'root': 0,
}

crazykit2_default = crazykit_default = presets["crazykit_2"] = presets["crazykit_default"] = {
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