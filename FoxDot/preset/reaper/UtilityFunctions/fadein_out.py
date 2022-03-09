
from FoxDot import Clock, linvar, inf, player_method
from FoxDot.lib.Extensions.PyliveSmartParams import SmartTrack

@player_method
def fadein(self, dur=8, fvol=1, ivol=0):
    if "reatrack" in self.attr.keys() and isinstance(self.attr["reatrack"][0], SmartTrack):
        self.vol = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
    else:
        self.amplify = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
    return self

@player_method
def fadeout(self, dur=8, ivol=1, fvol=0):
    if "reatrack" in self.attr.keys() and isinstance(self.attr["reatrack"][0], SmartTrack):
        self.vol = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
    else:
        self.amplify = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
    return self

@player_method
def fadeoutin(self, dur=8, outdur=16, ivol=1, mvol=0, fvol=1):
    if "reatrack" in self.attr.keys() and isinstance(self.attr["reatrack"][0], SmartTrack):
        self.vol = linvar([ivol, mvol, mvol, fvol], [dur, outdur, dur, inf], start=Clock.mod(4))
    else:
        self.amplify = linvar([ivol, mvol, mvol, fvol], [dur, outdur, dur, inf], start=Clock.mod(4))
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
