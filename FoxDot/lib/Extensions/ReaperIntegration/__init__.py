
from typing import Mapping
from pprint import pprint

from FoxDot.lib import Clock, player_method

from .ReaperInstruments import ReaperInstrumentFacade
from FoxDot.lib.Extensions.DynamicReaperParams import ReaProject, ReaTrack

reapy_project = None
project = None

#try:
project = ReaProject(Clock)
pass
# except Exception as err:
#     output = err.message if hasattr(err, 'message') else err
#     print("Error scanning and initializing Reaper project: {output} -> skipping Reaper integration".format(output=output))

class ReaperInstrumentFactory:

    def __init__(self, presets: Mapping, project: ReaProject) -> None:
        self._presets = presets
        self._project = project

    def create_instruc(self, *args, **kwargs):
        """handle exceptions gracefully especially if corresponding track does not exist in Live"""
        try:
            result = ReaperInstrumentFacade(Clock, self._project, self._presets, *args, **kwargs)
            return result.out
        except Exception as err:
            output = err.message if hasattr(err, 'message') else err
            print("Error creating instruc {name}: {output} -> skipping".format(name=kwargs["track_name"], output=output))
            return None

    def instruments_to_instanciate(self):
        rproject: ReaProject = self._project
        instrument_dict = {}

        for reatrack in rproject.bus_tracks:
            instrument_dict[reatrack.name[1:]] = self.create_instruc(track_name=reatrack.name, midi_channel=-1)

        # rproject.set_send_ids(rproject.sends)

        # sends_kwargs = {
        #     "track_name": "sends",
        #     "midi_channel": -1,
        # }
        # instrument_dict["sends"] = self.create_instruc(**sends_kwargs)

        for i, track in enumerate(rproject.instrument_tracks):
            instrument_kwargs = {
                "track_name": track.name,
                "midi_channel": i + 1,
            }
            instrument_dict[track.name] = self.create_instruc(**instrument_kwargs)

        return instrument_dict


@player_method
def setp(self, param_dict):
    for key, value in param_dict.items():
        setattr(self, key, value)

@player_method
def getp(self, filter = None):
    result = None
    if "reatrack" in self.attr.keys():
        smart_track = self.attr["reatrack"][0]
        if isinstance(smart_track, ReaTrack):
            result = smart_track.config
            if filter is not None:
                result = {key: value for key, value in smart_track.getp().items() if filter in key}
            else:
                result = smart_track.getp()
    return result

@player_method
def showp(self, filter = None):
    pprint(self.getp(filter))

@player_method
def get_send(self, send_num):
    if "reatrack" in self.attr.keys():
        smart_track = self.attr["reatrack"][0]
        if isinstance(smart_track, ReaTrack):
            return smart_track.get_send(send_num)

@player_method
def set_send(self, send_num, value):
    if "reatrack" in self.attr.keys():
        smart_track = self.attr["reatrack"][0]
        if isinstance(smart_track, ReaTrack):
            return smart_track.set_send(send_num, value)