# Pattern function
from .TimeVar import sinvar

def interpolate(start, end, step=6, go_back=True):
    assert len(start) == len(end)
    diffs = []
    result = []
    for i in range(len(start)):
        diffs += [start[i] - end[i]]
    base_pattern = start
    for j in range(step):
        new_pattern = [ e - diffs[k]/(step+1) for k, e in enumerate(base_pattern)]
        result.append(new_pattern)
        base_pattern = new_pattern
    if not go_back:
        result = [start] + result + [end]
    else:
        result = [start] + result + [end] + result[::-1] # result except last elem + end + reversed result

# Param shortcut functions to use with dict unpack : **lpf(linvar([0,.3],8))

def delay_clockless(clock, config=None, vol=None, time=None, feedback=None, pan=None, dry=None):
    delay_base = { "delay_vol": 0, "delay_time": .5, "delay_feedback": .5, "delay_pan": .5, "delay_dry": 1 }
    if config and 'var' in config:
        dur = int(config[3:])
        vol = sinvar([0,.6],dur)
        time = 1 / (clock.bpm / 60) # synchro delay time with current bpm
    vol = vol if vol is not None else delay_base["delay_vol"]
    time = time if time is not None else delay_base["delay_time"]
    feedback = feedback if feedback is not None else delay_base["delay_feedback"]
    pan = pan if pan is not None else delay_base["delay_pan"]
    dry = dry if dry is not None else delay_base["delay_dry"]
    return { "delay_vol": vol, "delay_time": time, "delay_feedback": feedback, "delay_pan": pan, "delay_dry": dry}

def lpf(freq, low_vol=0):
    return { "eq_gainlo": low_vol, "eq_freqlo": freq }

def tb3(config=None, decay=None, freq=None, reso=None, drive=None, delay=None):
    default_conf = { "i_decay":.33, "i_freq":.15, "i_reso": .66, "i_drive": .4, "i_delay": 0 }
    return default_conf

def set_bpm_clockless(clock, liveset, bpm=120):
    pass