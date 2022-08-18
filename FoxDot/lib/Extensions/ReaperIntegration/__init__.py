
from typing import Mapping
from pprint import pprint

from FoxDot.lib import Clock, player_method

from .ReaperInstruments import ReaperInstrumentFacade
from FoxDot.lib.Extensions.DynamicReaperParams import ReaProject, ReaTrack

#project = None

def init_reapy_project():
    project = None
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
        self._reaproject = project
        self.used_track_indexes = []

    def create_instrument(self, *args, **kwargs):
        """handle exceptions gracefully especially if corresponding track does not exist in Reaper"""
        try:
            return ReaperInstrumentFacade(self._reaproject, self._presets, *args, **kwargs)
        except Exception as err:
            output = err.message if hasattr(err, 'message') else err
            print("Error creating instruc {name}: {output} -> skipping".format(name=kwargs["track_name"], output=output))
            return None

    def instruments_to_instanciate(self):
        instrument_dict = {}

        for reatrack in self._reaproject.bus_tracks:
            instrument_dict[reatrack.name[1:]] = self.create_instrument(track_name=reatrack.name, midi_channel=-1)

        for i, track in enumerate(self._reaproject.instrument_tracks):
            instrument_kwargs = {
                "track_name": track.name,
                "midi_channel": i + 1,
            }
            instrument_dict[track.name] = self.create_instrument(**instrument_kwargs)

        return instrument_dict

    def add_instrument(self, name, plugin_name, preset=None, params={}, scan_all_params=False):
        free_indexes = [index for index in range(1,17) if index not in self.used_track_indexes]
        free_index = free_indexes[0]
        if preset is None:
            preset = name
        self.used_track_indexes.append(free_index)
        return self.create_instrument(
            track_name='chan'+str(free_index),
            midi_channel=free_index,
            create_instrument=True,
            instrument_name=name,
            plugin_name=plugin_name,
            plugin_preset=preset,
            instrument_params=params,
            scan_all_params=scan_all_params
        )

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