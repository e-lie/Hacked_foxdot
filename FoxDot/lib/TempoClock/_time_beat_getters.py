
def set_cpu_usage(self, value):
    """ Sets the `sleep_time` attribute to values based on desired high/low/medium cpu usage """
    assert 0 <= value <= 2
    self.sleep_time = self.sleep_values[value]
    return

def set_latency(self, value):
    """ Sets the `latency` attribute to values based on desired high/low/medium latency """
    assert 0 <= value <= 2
    self.latency = self.latency_values[value]
    return

def bar_length(self):
    """ Returns the length of a bar in terms of beats """
    return (float(self.meter[0]) / self.meter[1]) * 4

def bars(self, n=1):
    """ Returns the number of beats in 'n' bars """
    return self.bar_length() * n

def beat_dur(self, n=1):
    """ Returns the length of n beats in seconds """

    return 0 if n == 0 else (60.0 / self.get_bpm()) * n

def beats_to_seconds(self, beats):
    return self.beat_dur(beats)

def seconds_to_beats(self, seconds):
    """ Returns the number of beats that occur in a time period  """
    return (self.get_bpm() / 60.0) * seconds

