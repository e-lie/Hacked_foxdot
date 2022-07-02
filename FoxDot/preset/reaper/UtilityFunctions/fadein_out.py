
from FoxDot import Clock, linvar, sinvar, PWhite, PRand, inf, player_method
from FoxDot.lib.Extensions.DynamicReaperParams import ReaTrack

@player_method
def fadein(self, dur=8, fvol=1, ivol=0):
    if "reatrack" in self.attr.keys() and isinstance(self.attr["reatrack"][0], ReaTrack):
        self.vol = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
    else:
        self.amplify = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
    return self

@player_method
def fadeout(self, dur=8, ivol=1, fvol=0):
    if "reatrack" in self.attr.keys() and isinstance(self.attr["reatrack"][0], ReaTrack):
        self.vol = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
    else:
        self.amplify = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
    return self

@player_method
def fadeoutin(self, dur=8, outdur=16, ivol=1, mvol=0, fvol=1):
    if "reatrack" in self.attr.keys() and isinstance(self.attr["reatrack"][0], ReaTrack):
        self.vol = linvar([ivol, mvol, mvol, fvol], [dur, outdur, dur, inf], start=Clock.mod(4))
    else:
        self.amplify = linvar([ivol, mvol, mvol, fvol], [dur, outdur, dur, inf], start=Clock.mod(4))
    return self

@player_method
def fadeinout(self, dur=8, outdur=16, ivol=0, mvol=1, fvol=0):
    if "reatrack" in self.attr.keys() and isinstance(self.attr["reatrack"][0], ReaTrack):
        self.vol = linvar([ivol, mvol, mvol, fvol], [dur, outdur, dur, inf], start=Clock.mod(4))
    else:
        self.amplify = linvar([ivol, mvol, mvol, fvol], [dur, outdur, dur, inf], start=Clock.mod(4))
    return self

@player_method
def faderand(self, length=8):
    if "reatrack" in self.attr.keys() and isinstance(self.attr["reatrack"][0], ReaTrack):
        self.vol = sinvar([0] | PWhite(.2,1.2)[:length-1], [8] | PRand(1,4)[:length-1]*4, start=Clock.mod(4))
    else:
        self.amplify = sinvar([0] | PWhite(.2,1.2)[:length-1], [8] | PRand(1,4)[:length-1]*4, start=Clock.mod(4))
    return self
    


def fadein(dur=8, fvol=1, ivol=0):
    return {"vol": linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))}

def fadeout(dur=8, ivol=1, fvol=0):
    return {"vol": linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))}

def fadeoutin(dur=8, outdur=16, ivol=1, mvol=0, fvol=1):
    return {"vol": linvar([ivol, mvol, mvol, fvol], [dur, outdur, dur, inf], start=Clock.mod(4))}

@player_method
def sfadeout(self, dur=16, ivol=1, fvol=0):
    for player in list(self.metro.playing):
        if player is not self:
            player.fadeout(dur, ivol, fvol)
    return self

@player_method
def sfadein(self, dur=16, fvol=1, ivol=0):
    for player in list(self.metro.playing):
        if player is not self:
            player.fadein(dur, fvol, ivol)
    return self
