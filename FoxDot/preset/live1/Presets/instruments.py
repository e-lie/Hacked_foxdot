from .effects import *

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
