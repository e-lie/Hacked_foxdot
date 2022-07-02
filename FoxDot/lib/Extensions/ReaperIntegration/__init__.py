
from typing import Mapping
from pprint import pprint

from FoxDot.lib import Clock, player_method

from .ReaperInstruments import ReaperInstrumentFacade
from FoxDot.lib.Extensions.DynamicReaperParams import ReaProject, ReaTrack

#project = None

def init_reapy_project():
    try:
        import reapy
        project = ReaProject(Clock, reapy)

    except Exception as err:
        output = err.message if hasattr(err, 'message') else err
        print("Error scanning and initializing Reaper project: {output} -> skipping Reaper integration".format(output=output))
    return project

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
        reatrack = self.attr["reatrack"][0]
        if isinstance(reatrack, ReaTrack):
            #result = reatrack.config
            if filter is not None:
                result = {key: value for key, value in reatrack.get_all_params().items() if filter in key}
            else:
                result = reatrack.get_all_params()
    return result

@player_method
def showp(self, filter = None):
    pprint(self.getp(filter))