from FoxDot import Pvar

class ParamRange:

    def __init__(self, start, stop, value):
        print(start, stop)
        assert start < stop, "A param range should have start < stop"
        self.start = start
        self.stop = stop
        self.value = value

    def __repr__(self):
        return f"<ParamRange {self.start} {self.stop} - {self.value}>"

    def __eq__(self, other):
        return self.start == other.start and self.stop == other.stop

    def __lt__(self, other): # to make it sortable
        return self.start < other.start

    def __hash__(self):
        return hash((self.start, self.stop, self.value))

    def overlap(self, other):
        disjoint_1 = self.start < other.start and self.stop <= other.start
        disjoint_2 = other.start < self.start and other.stop <= self.start
        return not (disjoint_1 or disjoint_2)

    def boolean_union(self, other):
        assert self.overlap(other), "Ranges should overlap to execute boolean operation"
        if self.start >= other.start and other.stop >= self.stop:
            return [ParamRange(other.start, other.stop, other.value)]
        elif self.start < other.start and self.stop <= other.stop:
            return [
                ParamRange(self.start, other.start, self.value),
                ParamRange(other.start, other.stop, other.value)
            ]
        elif self.start < other.start and self.stop > other.stop:
            return [
                ParamRange(self.start, other.start, self.value),
                ParamRange(other.start, other.stop, other.value),
                ParamRange(other.stop, self.stop, self.value),
            ]
        elif other.start < self.start and other.stop < self.stop:
            return [
                ParamRange(other.start, other.stop, other.value),
                ParamRange(other.stop, self.stop, self.value),
            ]
        else:
            raise Exception()

class ParamTimeline:

    def __init__(self, duration, value):
        self.base = value
        self.param_ranges = [ParamRange(0, duration, value)]
        self.duration = duration

    def add_value_range(self, new_pr: ParamRange):
        assert new_pr.start >= 0 and new_pr.stop <= self.duration, "new range should be inside total timeline range"
        new_param_ranges = []
        for pr in self.param_ranges:
            if pr.overlap(new_pr):
                new_param_ranges += pr.boolean_union(new_pr)
            else:
                new_param_ranges.append(pr)
        self.param_ranges = list(set(new_param_ranges))
        self.param_ranges.sort()

    def __add__(self, other):
        assert isinstance(other, tuple) and len(other) == 3, "add operator for param range works with tuples of length 3"
        self.add_value_range(ParamRange(other[0], other[1], other[2]))
        return self

    def __repr__(self):
        return f"<ParamTimeline {self.param_ranges}>"

    def out(self):
        values = [pr.value for pr in self.param_ranges]
        durations = [pr.stop - pr.start for pr in self.param_ranges]
        return Pvar(values, durations)



Pt = ParamTimeline




