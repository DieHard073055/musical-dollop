import json
import plistlib
from pathlib import Path
from typing import List, Dict, Any


def json_serializable(o: Any) -> str:
    return str(o)


def parse_file(file: Path) -> Dict[str, Any]:
    playlist = dict()
    with open(file, 'rb') as itunes_playlist_file:
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
    duplicates = [track_ids for track_name, track_ids in track_duplicates_counter.items() if len(track_ids) > 1]

    return duplicates


def get_tracks(playlist: List[Dict[str, Any]]) -> List[str]:
    return [track["Name"] for track_id, track in playlist.items()]


def find_common_tracks(playlist_1, playlist_2):
    tracks_pl_1 = get_tracks(playlist_1)
    tracks_pl_2 = get_tracks(playlist_2)

    return list(set(tracks_pl_1).intersection(tracks_pl_2))




