
reverb_default = {
    "reverb_dw": 0,
    "reverb_hifreq": .89,
    "reverb_lowfreq": .11,
    "reverb_decay": .41,
}

resob_default = {
    "resob_dw": 0,
    "resob_color": .85,
    "resob_gain": .66,
    "resob_width": 1,
}

eq_default = {
    "eq_gainlo": .85,
    "eq_gainmid": .85,
    "eq_gainhi": .85,
    "eq_freqlo": .3,
    "eq_freqhi": .57,
}

delay_default = {
    "delay_vol": 0,
    "delay_time": 0,
    "delay_feedback": .5,
    "delay_pan": .9,
    "delay_dry": 1,
}

hamp_default = {
    "hamp_dw": 0,
    "hamp_gain": .47,
    "hamp_low": .68,
    "hamp_mid": .68,
    "hamp_high": .6,
    "hamp_cabinet": .23,
    "hamp_vol": .68,
    "hamp_rack_vol": .83,
}

phaser_default = {
    "phaser_dw": 0,
    "phaser_drive": 0,
    "phaser_width": 1,
    "phaser_reso": 1,
    "phaser_phase": .9,
    "phaser_lfo1": .3,
    "phaser_lfo2": .3,
    "phaser_lfo3": .5,
}

config_default = {} | reverb_default | eq_default | resob_default | delay_default | hamp_default | phaser_default
