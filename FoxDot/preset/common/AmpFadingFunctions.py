# Pattern function
from copy import Error

import math
from FoxDot import Player, Group, Pvar, player_method, PWhite, linvar, inf, Clock, TimeVar, var, expvar, sinvar, Pattern, xvar, yvar


# def ampfadein(dur=4, famp=.8, iamp=0):
#     return {"amplify": linvar([iamp, famp], [dur, inf], start=Clock.mod(4))}

# def ampfadeout(dur=16, iamp=.8, famp=0):
#     return {"amplify": linvar([iamp, famp], [dur, inf], start=Clock.mod(4))}

@player_method
def ampfadein(self, dur=4, famp=.8, iamp=0):
    # if iamp == None:
        # iamp = self.amplify
    self.amplify = linvar([iamp, famp], [dur, inf], start=Clock.mod(4))

@player_method
def ampfadeout(self, dur=4, famp=0, iamp=.8):
    # if iamp == None:
        # iamp = self.amplify
    self.amplify = linvar([iamp, famp], [dur, inf], start=Clock.mod(4))

@player_method
def sampfadeout(self, dur=16, iamp=0, famp=0):
    for player in list(self.metro.playing):
        if player is not self and not player.always_on:
            player.ampfadeout(dur, iamp, famp)
    return self

@player_method
def sampfadein(self, dur=16, famp=.8, iamp=0):
    for player in list(self.metro.playing):
        if player is not self:
            player.ampfadein(dur, famp, iamp)
    return self

# @player_method
# def generic_fadeout(self, dur=8, ivol=1, fvol=0):
#     self.amplify = linvar([ivol, fvol], [dur, inf], start=Clock.mod(4))
#     return self
