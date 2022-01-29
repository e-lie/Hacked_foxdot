import live

from FoxDot.lib import Clock

from .SmartSetParams import SmartSet
from .AbletonInstruments import AbletonInstrumentFacade

liveset = live.Set()

try:
    liveset.scan(scan_clip_names=True, scan_devices=True)
    smartset = SmartSet(Clock, liveset)
except Exception as err:
    output = err.message if hasattr(err, 'message') else err
    print("Error scanning and initializing  ableton liveset: {output} -> skipping ableton integration".format(output=output))


def arm_all():
    for track in liveset.tracks:
        track.arm = 1

def create_instruc(*args, **kwargs):
    """handle exceptions gracefully especially if corresponding track does not exist in Live"""
    try:
        result = AbletonInstrumentFacade(Clock, smartset, *args, **kwargs)
        return result.out
    except Exception as err:
        output = err.message if hasattr(err, 'message') else err
        print("Error creating instruc {name}: {output} -> skipping".format(name=kwargs["track_name"], output=output))
        return None