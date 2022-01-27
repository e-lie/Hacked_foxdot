# Pattern function
from copy import Error
from .TimeVar import linvar, sinvar, Pvar, PWhite, Pattern, inf
from . import Clock, nextBar
from .InstrumentPreset import liveset


def interpolate(start, end, step=6, go_back=True):
    assert len(start) == len(end)
    diffs = []
    result = []
    for i in range(len(start)):
        diffs += [start[i] - end[i]]
    base_pattern = start
    for j in range(step):
        new_pattern = [e - diffs[k] / (step + 1)
                       for k, e in enumerate(base_pattern)]
        result.append(new_pattern)
        base_pattern = new_pattern
    if not go_back:
        result = [start] + result + [end]
    else:
        result = (
            [start] + result + [end] + result[::-1]
        )  # result except last elem + end + reversed result
    return result


# Param shortcut functions to use with dict unpack : **lpf(linvar([0,.3],8))

# def delay(config=None, vol=None, time=None, feedback=None, pan=None, dry=None):
#     delay_base = { "delay_vol": 0, "delay_time": .5, "delay_feedback": .5, "delay_pan": .5, "delay_dry": 1 }
#     if config and 'var' in config:
#         dur = int(config[3:])
#         vol = sinvar([0,.6],dur)
#         time = 1 / (Clock.bpm / 60) # synchro delay time with current bpm
#     vol = vol if vol is not None else delay_base["delay_vol"]
#     time = time if time is not None else delay_base["delay_time"]
#     feedback = feedback if feedback is not None else delay_base["delay_feedback"]
#     pan = pan if pan is not None else delay_base["delay_pan"]
#     dry = dry if dry is not None else delay_base["delay_dry"]
#     return { "delay_vol": vol, "delay_time": time, "delay_feedback": feedback, "delay_pan": pan, "delay_dry": dry}


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


def set_bpm_clockless(clock, liveset, bpm=120):
    pass


def zipvar(duration_pattern_list):
    if len(duration_pattern_list) == 1:
        return duration_pattern_list[0][0]
    patterns = [item[0] for item in duration_pattern_list]
    durations = [item[1] for item in duration_pattern_list]
    return Pvar(patterns, durations)


# def pattern_tweak(pattern, tweak_len=None, config="random", random_amount=.1, compensation=True):
#     plen = len(pattern)
#     tweak_len = tweak_len if tweak_len else plen-1
#     assert plen > 1

#     if config == "random":
#         tweak_serie = PWhite(-random_amount,random_amount)[:tweak_len]
#         print(tweak_serie)
#     else:
#         raise Error("This tweak pattern config doesn't exist : {}".format(config))

#     result = []
#     current_modulo = 0
#     total_tweak_amount = 0
#     for i, tweak_value in enumerate(tweak_serie):
#         current_modulo = i%plen
#         result.append(pattern[current_modulo] + tweak_value)
#         total_tweak_amount += tweak_value

#     if compensation:
#         print(current_modulo)
#         remaining_values = [value for value in pattern[(current_modulo+1+1)%plen:-1]]
#         print(remaining_values)
#         tweak_compensation_values = [-total_tweak_amount/len(remaining_values) for value in remaining_values]
#         result += tweak_compensation_values
#     print(result)
#     return result


def rnd(pattern, random_amount=0.05, compensation=True):
    tweak_serie = PWhite(-random_amount, random_amount)[: len(pattern)]
    result = [pattern[i] + tweak_serie[i] for i in range(len(pattern))]
    if compensation:
        result += [pattern[i] - tweak_serie[i] for i in range(len(pattern))]
    print(result)
    return result


def rnd1(pattern):
    average_value = sum(pattern) / len(pattern)
    return rnd(pattern, random_amount=0.1 * average_value)


def rnd2(pattern):
    average_value = sum(pattern) / len(pattern)
    return rnd(pattern, random_amount=0.2 * average_value)


def rnd5(pattern):
    average_value = sum(pattern) / len(pattern)
    return rnd(pattern, random_amount=0.05 * average_value)


def microshift(pattern, shifts):
    for key, value in shifts.items():
        if key in range(len(pattern) - 1):
            pattern[key] += value
            pattern[key + 1] -= value
    print(pattern)
    return pattern


def zipat(*args):
    notes = [item for i, item in enumerate(args) if i % 2 == 0]
    dur = [item for i, item in enumerate(args) if i % 2 == 1]
    return {"degree": notes, "dur": dur}


ZP = zipat


def fadein(dur=4, fvol=1, ivol=0):
    return {"vol": linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))}


def ampfadein(dur=4, famp=.8, iamp=0):
    return {"amp": linvar([iamp, famp], [dur, inf], start=Clock.mod(4))}


def ampfadeout(dur=16, iamp=.8, famp=0):
    return {"amp": linvar([iamp, famp], [dur, inf], start=Clock.mod(4))}


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
