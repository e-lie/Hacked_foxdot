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

phaser_default = presets["phaser_default"] = {
    "phaser_dw": 0,
    "phaser_drive": 0,
    "phaser_width": 1,
    "phaser_reso": 1,
    "phaser_phase": 0,
    "phaser_lfo1": .2,
    "phaser_lfo2": .4,
    "phaser_lfo3": 0,
}

phasers1 = {
    'phaser_drive': 0.984251968503937,
    'phaser_dw': 0.7244094488188977,
    'phaser_lfo1': 0.3228346456692913,
    'phaser_lfo2': 0.6929133858267716,
    'phaser_lfo3': 0.8661417322834646,
    'phaser_phase': 0.0,
    'phaser_reso': 1.0,
    'phaser_width': 1.0
}

lpf_default = presets["lpf_default"] = {
    'lpf_drive': 0.0,
    'lpf_dw': 1.0,
    'lpf_freq': 1.0,
    'lpf_input_gain': 0.8536585409810223,
    'lpf_lfo': 0.0,
    'lpf_lfo_phase': 0.0,
    'lpf_reso': 0.0,
    'lpf_volume': 0.8500000360443836
}

hpf_default = presets["hpf_default"] = {
    'hpf_drive': 0.0,
    'hpf_dw': 1.0,
    'hpf_freq': 0.0,
    'hpf_input_gain': 0.8536585409810223,
    'hpf_lfo': 0.0,
    'hpf_lfo_phase': 0.0,
    'hpf_reso': 0.0,
    'hpf_volume': 0.8500000360443836
}
