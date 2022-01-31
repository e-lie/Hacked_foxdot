
from FoxDot import Clock, linvar, inf, PWhite, nextBar, player_method
from FoxDot.lib.Extensions.Live import liveset
from FoxDot.lib.Extensions.PyliveSmartParams import set_smart_param


def delay(subdiv=1 / 2, vol=0.6, time=None, feedback=0.5, pan=0.5, dry=1):
    config = {
        "delay_vol": vol,
        "delay_feedback": feedback,
        "delay_pan": pan,
        "delay_dry": dry,
    }
    if time is not None:
        config["delay_time"] = time
    else:
        beat_dur = 1 / (Clock.bpm / 60)  # synchro delay time with current bpm
        config["delay_time"] = subdiv * beat_dur
    return config


def lpf(freq, low_vol=0):
    return {"eq_gainlo": low_vol, "eq_freqlo": freq}


def tb3(config=None, decay=None, freq=None, reso=None, drive=None, delay=None):
    default_conf = {
        "i_decay": 0.33,
        "i_freq": 0.15,
        "i_reso": 0.66,
        "i_drive": 0.4,
        "i_delay": 0,
    }
    return default_conf


@player_method
def fadein(self, dur=4, fvol=1, ivol=0):
    smart_track = self.attr["smart_track"][0]
    #change eq_gain to avoid conflict with volume (but for eq_gain .5 -> 0dB)
    set_smart_param(smart_track, "eq_gain", linvar([ivol/2, fvol/2], [dur, inf], start=Clock.mod(4)))
    return self


def fadein(dur=4, fvol=1, ivol=0):
    return {"vol": linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))}


def fadeout(dur=16, ivol=1, fvol=0):
    return {"vol": linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))}


def fadeoutin(dur=16, outdur=16, ivol=1, mvol=0, fvol=1):
    return {"vol": linvar([ivol, mvol, mvol, fvol], [dur, outdur, dur, inf], start=Clock.mod(4))}




def change_bpm(bpm, midi_nudge=True, nudge_base=0.22):
    Clock.bpm = bpm
    liveset.tempo = bpm

    @nextBar()
    def nudging():
        if midi_nudge:
            Clock.midi_nudge = 60 / bpm - nudge_base

def randomize_params(param_dict, seed=0):
    params_values = PWhite(seed=seed)[:len(param_dict.keys())]
    for i, key in enumerate(param_dict.keys()):
        param_dict[key] = params_values[i]
    return param_dict

rndp = randomize_params