import json
import plistlib
from pathlib import Path
from typing import List, Dict, Any
from matplotlib import pyplot
import numpy as np


def json_serializable(o: Any) -> str:
    return str(o)


def parse_file(file: Path) -> Dict[str, Any]:
    playlist = dict()
    with open(file, "rb") as itunes_playlist_file:
        playlist = itunes_playlist_file.read()
        playlist = plistlib.loads(playlist)
    return playlist


def get_duplicate_tracks(tracks: List[Dict[str, Any]]) -> List[List[Dict[str, Any]]]:
    track_duplicates_counter = dict()
    duplicates = []
    for track_id, track in tracks.items():
        if track["Name"] not in track_duplicates_counter.keys():
            track_duplicates_counter[track["Name"]] = []
        track_duplicates_counter[track["Name"]].append(track_id)
    duplicates = [
        track_ids
        for track_name, track_ids in track_duplicates_counter.items()
        if len(track_ids) > 1
    ]

    return duplicates


def get_tracks(playlist: List[Dict[str, Any]]) -> List[str]:
    return [track["Name"] for track_id, track in playlist.items()]


def find_common_tracks(playlist_1, playlist_2):
    tracks_pl_1 = get_tracks(playlist_1)
    tracks_pl_2 = get_tracks(playlist_2)

    return list(set(tracks_pl_1).intersection(tracks_pl_2))


def plot_statistics(tracks):
    ratings = []
    durations = []

    for track_id, track in tracks.items():
        try:
            ratings.append(track["Album Rating"])
            durations.append(track["Total Time"])
        except KeyError:
            # key album rating does not exist
            pass

    if durations != [] and ratings != []:
        durations_np = np.array(durations, np.int32)
        # convert to minutes
        durations_np = durations_np / 60000.0

        ratings_np = np.array(ratings, np.int32)

        pyplot.subplot(2, 1, 1)
        pyplot.plot(durations_np, ratings_np, "o")
        pyplot.axis([0, 1.05 * np.max(durations_np), -1, 110])
        pyplot.xlabel("Track duration")
        pyplot.ylabel("Track rating")
        # plot histogram
        pyplot.subplot(2, 1, 2)
        pyplot.hist(durations_np, bins=20)
        pyplot.xlabel("Track duration")
        pyplot.ylabel("Count")
        # show plot
        pyplot.show()
