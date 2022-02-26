


#sends_default = {
#    "sreverb": 0,
#    "ssc": 0,
#    "sgate": 0,
#    "swh": 0,
#    "swiden": 0,
#}

presets = {}
presets["track_default"] = {
    "vol": 1,
    "pan": 0,
    "amplify": .8,
}

presets["reverb_default"] = {
    "reverb_dw": 0,
    "reverb_hifreq": .89,
    "reverb_lowfreq": .11,
    "reverb_decay": .41,
}

presets["resob_default"] = {
    "resob_dw": 0,
    "resob_color": .85,
    "resob_gain": .66,
    "resob_width": 1,
}

presets["eq_default"] = {
    "eq_gainlo": .85,
    "eq_gainmid": .85,
    "eq_gainhi": .85,
    "eq_freqlo": .3,
    "eq_freqhi": .57,
    "eq_gain": .5,
    "eq_width": .5,
    "eq_pan": .5,
}

presets["delay_default"] = {
    "delay_vol": 0,
    "delay_time": 0,
    "delay_feedback": .5,
    "delay_pan": .9,
    "delay_dry": 1,
}

presets["hamp_default"] = {
    "hamp_dw": 0,
    "hamp_gain": .47,
    "hamp_low": .68,
    "hamp_mid": .68,
    "hamp_high": .6,
    "hamp_cabinet": .23,
    "hamp_vol": .68,
    "hamp_rack_vol": .83,
}

presets["phaser_default"] = {
    "phaser_dw": 0,
    "phaser_drive": 0,
    "phaser_width": 1,
    "phaser_reso": 1,
    "phaser_phase": .9,
    "phaser_lfo1": .3,
    "phaser_lfo2": .3,
    "phaser_lfo3": .5,
}


#presets["config_default"] = {} | reverb_default | eq_default | resob_default | delay_default | hamp_default | phaser_default

###########################################################
###########################################################
###########################################################




presets["reverb_default"] = {
    "reverb_dw": 0,
    "reverb_hifreq": 0,
    "reverb_lowfreq": 0,
    "reverb_decay": 0,
}

presets["resob_default"] = {
    "resob_dw": 0,
    "resob_color": 0,
    "resob_gain": 0,
    "resob_width": 0,
}

presets["phaser_default"] = {
    "phaser_lfo1": 0,
    "phaser_lfo2": 0,
    "phaser_lfo3": 0,
    "phaser_phase": 0,
    "phaser_reso": 0,
    "phaser_drive": 0,
    "phaser_width": 0,
    "phaser_dw": 0,
}

presets["hamp_default"] = {
 'hamp_cabinet': 0.236,
 'hamp_dw': 0.0,
 'hamp_gain': 0.46,
 'hamp_high': 0.603,
 'hamp_low': 0.66,
 'hamp_mid': 0.667,
 'hamp_rack_vol': 0.85,
 'hamp_vol': 0.625,
}

################################################################
################################################################
##################    Instruments params     ###################
################################################################
################################################################


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
