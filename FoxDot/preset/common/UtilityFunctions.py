# Pattern function
from copy import Error

import math
from FoxDot import Pvar, player_method, PWhite, linvar, inf, Clock, TimeVar, var, expvar, sinvar, Pattern, xvar, yvar


def interpolate(start, end, step=7, go_back=False):
    if len(start) == 1 and len(end) > 1:
        start = [start[0]] * len(end)
    if len(end) == 1 and len(start) > 1:
        end = [end[0]] * len(start)
    assert len(start) == len(end)
    diffs = []
    result = []
    for i in range(len(start)):
        diffs += [start[i] - end[i]]
    base_pattern = start
    for j in range(step):
        new_pattern = [
            e - diffs[k]/(step + 1) for k, e in enumerate(base_pattern)
        ]
        result.append(new_pattern)
        base_pattern = new_pattern
    if not go_back:
        result = [start] + result + [end]
    else:
        result = (
            [start] + result + [end] + result[::-1]
        )  # result except last elem + end + reversed result
    return result


interp = interpolate

def interpvar(start, end, total_dur=None, step=6, dur=1, go_back=False):
    if total_dur is not None:
        step = (total_dur - 2) // 2
        dur = 1
    return Pvar(interpolate(start, end, step, go_back), dur)


Pvi = interpvar

def interP(start, end, repeat=1, step=6):
    res = Pattern([])
    for pattern in interpolate(start, end, step, go_back=True):
        for i in range(repeat):
            res = res | pattern
    return res

def interPBof2(start, end, repeat=1, step=6, go_back=True):
    res = Pattern([])
    for pattern in interpolate(start, end, step, go_back):
        for i in range(repeat):
            res = res | pattern
    pprint(res)
    if not go_back:
        for i in range(10):
            res = res | Pattern(end)
        total_dur = sum(res)
        print(total_dur)
        return Pvar([res, end], [int(total_dur)-1, inf], start=Clock.mod(4))
    else:
        return res

# def interPBof(start, end, step=6, total_dur=None,  dur=4, go_back=False):
#     if total_dur is not None:
#         step = (total_dur - 2) // 2
#         dur = 4
#     patterns = interpolate(start, end, step, go_back)
#     if not go_back:
#         res = Pvar(patterns, [dur]*(len(patterns)-1) + [inf], start=Clock.now())
#     else:
#         res = Pvar(patterns, [dur], start=Clock.now())
#     return res


def zipvar(duration_pattern_list):
    if len(duration_pattern_list) == 1:
        return duration_pattern_list[0][0]
    patterns = [item[0] for item in duration_pattern_list]
    durations = [item[1] for item in duration_pattern_list]
    return Pvar(patterns, durations)


Pvz = zipvar


def Pzr(root_pattern_list):
    if len(root_pattern_list) == 1:
        return {
            "degree": root_pattern_list[0][0],
            "root": root_pattern_list[0][1]
        }
    patterns = [item[0] for item in root_pattern_list]
    roots = [item[1] for item in root_pattern_list]
    durations = [item[2] for item in root_pattern_list]
    return {"degree": Pvar(patterns, durations), "root": Pvar(roots, durations)}

# Param shortcut functions to use with dict unpack : **lpf(linvar([0,.3],8))

@player_method
def humz(self, velocity=20, humanize=5, swing=0):
    """ Humanize the velocity, delay and add swing in % (less to more)"""
    humanize += 0.1
    if velocity!=0:
        self.delay=[0,PWhite((-1*humanize/100)*self.dur, (humanize/100)*self.dur) + (self.dur*swing/100)]
        self.amplify=[1,PWhite((100-velocity)/100,1)]
    else:
        self.delay=0
        self.amplify=1
    return self

def bpmto(new_bpm, duration=16):
    old_bpm = Clock.bpm
    return linvar([old_bpm, new_bpm], [duration, inf], start=Clock.mod(4))


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



def ampfadein(dur=4, famp=.8, iamp=0):
    return {"amplify": linvar([iamp, famp], [dur, inf], start=Clock.mod(4))}

def ampfadeout(dur=16, iamp=.8, famp=0):
    return {"amplify": linvar([iamp, famp], [dur, inf], start=Clock.mod(4))}

@player_method
def ampfadein(self, dur=4, famp=.8, iamp=0):
    self.amplify = linvar([iamp, famp], [dur, inf], start=Clock.mod(4))

@player_method
def ampfadeout(self, dur=4, iamp=.8, famp=0):
    self.amplify = linvar([iamp, famp], [dur, inf], start=Clock.mod(4))

@player_method
def sampfadeout(self, dur=16, iamp=.8, famp=0):
    for player in list(self.metro.playing):
        if player is not self:
            player.ampfadeout(dur, iamp, famp)
    return self

@player_method
def sampfadein(self, dur=16, famp=.8, iamp=0):
    for player in list(self.metro.playing):
        if player is not self:
            player.ampfadein(dur, famp, iamp)
    return self

def run_now(f):
    f()
    return f

# This is not really a decorator, more a currying mechanism using the decorator syntax
# Cf: https://www.geeksforgeeks.org/currying-function-in-python/ and https://www.saltycrane.com/blog/2010/03/simple-python-decorator-examples/


def later_clockless(clock):
    def later_clocked(future_dur):
        def later_decorator(f):
            clock.future(future_dur, f)
            return f
        return later_decorator
    return later_clocked


def hexa_panning_beta(value):
    value = value % 6
    # continous panning between front speakers
    output = 2
    pan = 0
    if value >= 0 and value <= 1:
        output = 2
        pan = value * 2 - 1
    # brutal jump to rear right speaker because there no way to make continuous transition
    # without left right independant volume
    elif value > 1 and value < 2:
        output = 4
        pan = -1
    # continuous panning between rear right speakers
    elif value >= 2 and value <= 3:
        output = 4
        pan = (value-2) * 2 - 1
    # brutal jump to rear left speaker because there no way to make continuous transition
    # without left right independant volume
    elif value > 3 and value < 4:
        output = 6
        pan = -1
    # continuous panning between rear left speakers
    elif value >= 4 and value <= 5:
        output = 6
        pan = (value-4) * 2 - 1
    # brutal jump to left speaker because there no way to make continuous transition
    # without left right independant volume
    elif value > 5 and value < 6:
        output = 2
        pan = -1
    return {"output": output, "pan": pan}

def hexa_panning_beta_old(value): # for interleaved speakers (less intuitive)
    value = value % 6
    # continous panning between front speakers
    output = 2
    pan = 0
    if value >= 0 and value <= 1:
        output = 2
        pan = value * 2 - 1
    # brutal jump to right speaker because there no way to make continuous transition
    # without left right independant volume
    elif value > 1 and value < 3:
        output = 4
        pan = -1
    # continuous panning between rear speakers
    elif value >= 3 and value <= 4:
        output = 6
        pan = 1 - (value - 3) * 2
    # brutal jump to left speaker because there no way to make continuous transition
    # without left right independant volume
    elif value > 4 and value < 6:
        output = 4
        pan = 1
    return {"output": output, "pan": pan}

def hexa_panning_timevar_beta(entry: TimeVar):
    output = 2
    pan = 0
    output_values = []
    pan_values = []
    for value in entry.values:
        output_values.append(hexa_panning_beta(value)["output"])
        pan_values.append(hexa_panning_beta(value)["pan"])
        output = var(values=output_values, dur=entry.dur, start=entry.start_time)
    if isinstance(entry, linvar):
        pan = linvar(values=pan_values, dur=entry.dur, start=entry.start_time)
    elif isinstance(entry, sinvar):
        pan = sinvar(values=pan_values, dur=entry.dur, start=entry.start_time)
    elif isinstance(entry, expvar):
        pan = expvar(values=pan_values, dur=entry.dur, start=entry.start_time)
    elif isinstance(entry, TimeVar) and not isinstance(entry, Pvar):
        pan = var(values=pan_values, dur=entry.dur, start=entry.start_time)
    return {"output": output, "pan": pan}


def hexa_panning_simple_pattern(entry: Pattern):
    output_pattern = []
    pan_pattern = []
    for value in entry:
        output_pattern.append(hexa_panning_beta(value)["output"])
        pan_pattern.append(hexa_panning_beta(value)["pan"])
    result = {"output": output_pattern, "pan": pan_pattern}
    return result

@player_method
def mpan(self, entry):
    if isinstance(entry, TimeVar):
        res = hexa_panning_timevar_beta(entry)
        self.pan = res["pan"]
        self.output = res["output"]
        return self
    elif not hasattr(entry, '__iter__') or isinstance(entry, tuple):
        entry = Pattern(entry)
    res = hexa_panning_simple_pattern(entry)
    self.pan = res["pan"]
    self.output = res["output"]
    return self

def mpan(entry):
    if isinstance(entry, TimeVar):
        return hexa_panning_timevar_beta(entry)
    elif not hasattr(entry, '__iter__') or isinstance(entry, tuple):
        entry = Pattern(entry)
    return hexa_panning_simple_pattern(entry)


def surround_panning(position=0, distance=1):
    position = (position + 4) % 6  # first speaker is at 240 degree (fifth speaker => 4 counting from 0)
    degree = -1 * position / 6.0 * 360
    surx = math.cos(math.radians(degree))
    sury = math.sin(math.radians(degree))
    # the circle is at center .5/.5 and r = distance/2
    sury = distance * 1 / 2 * sury + .5
    surx = distance * 1 / 2 * surx + .5
    return {"sur_x": surx, "sur_y": sury}


def surpan(position, distance=1):
    if isinstance(position, linvar):
        values = [ (value % 6) * 60 for value in position.values ]
        print(values)
        surx = xvar(values=values, dur=position.dur, start=position.start_time)
        sury = yvar(values=values, dur=position.dur, start=position.start_time)
        sury = distance * 1 / 2 * sury + .5
        surx = distance * 1 / 2 * surx + .5
    elif isinstance(position, TimeVar):
        xy_values = [surround_panning(pos, distance) for pos in position.values]
        surx = var(values=[elem["sur_x"] for elem in xy_values], dur=position.dur, start=position.start_time)
        sury = var(values=[elem["sur_y"] for elem in xy_values], dur=position.dur, start=position.start_time)
    else:
        surx = surround_panning(position, distance)["sur_x"]
        sury = surround_panning(position, distance)["sur_y"]
    return {"sur_x": surx, "sur_y": sury}

@player_method
def span(self, position, distance=1):
    res = surpan(position, distance)
    self.sur_x = res["sur_x"]
    self.sur_y = res["sur_y"]
    return self


base_mpan_dict = {
    0: {
        "output": 2,
        "pan": -1
    },
    1: {
        "output": 2,
        "pan": 1
    },
    2: {
        "output": 4,
        "pan": -1
    },
    3: {
        "output": 6,
        "pan": 1
    },
    4: {
        "output": 6,
        "pan": -1
    },
    5: {
        "output": 4,
        "pan": 1
    },
}

def surotate(dur=4):
    sury = sinvar([0,1], 4)
    return {"sur_x": 1, "sur_y": 1}