from enum import Enum


class ReaParamState(Enum):
    NORMAL = 0
    VAR1 = 1
    VAR2 = 2


class ReaParam(object):
    def __init__(self, name, value, index=None, reaper_name=None, state=ReaParamState.NORMAL):
        self.name = name
        self.index = index
        self.value = value
        self.reaper_name = reaper_name
        self.state: ReaParamState = state


class ReaSend(ReaParam):
    def set_value(self, track, value):
        # use value /2 to have vol 1 <=> not max but 0 Db
        # Plus convert vol logarithmic value to linear 0 -> 1 value
        self.value = value
        # track.sends[self.index].volume = 5*float(self.value/2)**2.5
        track.sends[self.index].volume = self.value

    def __repr__(self):
        return f"<ReaSend idx: {self.index} - {self.value}>"


class ReaSendTreeNode(ReaParam):
    """
    Binary tree of sends to quickly set balanced volumes for multiple (effect) busses: example
    (global) volume .8, mix .6, submix1 .2, submix2 .8
    => send11 0.256 send12 0.064 send21 0.096 send22 0.384 => total = .8
    """
    def __init__(self, children1, children2=[], mix=0, value=1, state=ReaParamState.NORMAL):
        self.state = state
        self.mix = mix
        self.value = value
        if len(children1) <= 1:
            self.child1 = ReaSend(name=None, index=children1[0].index, value=children1[0].volume)
        else:
            self.child1 = ReaSendTreeNode(
                children1=children1[:len(children1)-len(children1)//2],
                children2=children1[len(children1)-len(children1)//2:],
            )
        if len(children2) <= 1:
            self.child2 = ReaSend(name=None, index=children2[0].index, value=children2[0].volume)
        else:
            self.child2 = ReaSendTreeNode(
                children1=children2[:len(children2)-len(children2)//2],
                children2=children2[len(children2)-len(children2)//2:],
            )

    def set_value(self, track, value):
        self.value = value
        # Recursively set child 1 vol
        if isinstance(self.child1, ReaSendTreeNode):
            self.child1.set_value(track, self.value*(1-self.mix))
        elif isinstance(self.child1, ReaSend): # child1 is a reapy send from self.track.sends
            self.child1.set_value(track, self.value*(1-self.mix))
        else:
            raise Exception("Problem with the built ReaSendTree")
        # Recursively set child 2 vol
        if isinstance(self.child2, ReaSendTreeNode):
            self.child2.set_value(track, self.value*self.mix)
        elif isinstance(self.child2, ReaSend): # child1 is a reapy send from self.track.sends
            self.child2.set_value(track, self.value*self.mix)
        else:
            raise Exception("Problem with the built ReaSendTree")

    def set_mix(self, track, value):
        self.mix = value
        # Recursively set child 1 vol
        if isinstance(self.child1, ReaSendTreeNode):
            self.child1.set_value(track, self.value*(1-self.mix))
        elif isinstance(self.child1, ReaSend): # child1 is a reapy send from self.track.sends
            self.child1.set_value(track, self.value*(1-self.mix))
        else:
            raise Exception("Problem with the built ReaSendTree")
        # Recursively set child 2 vol
        if isinstance(self.child2, ReaSendTreeNode):
            self.child2.set_value(track, self.value*self.mix)
        elif isinstance(self.child2, ReaSend): # child1 is a reapy send from self.track.sends
            self.child2.set_value(track, self.value*self.mix)
        else:
            raise Exception("Problem with the built ReaSendTree")



    def __repr__(self):
        return f"<ReaSendTreeNode vol{self.value} - mix{self.mix} - {self.child1} - {self.child2}>"