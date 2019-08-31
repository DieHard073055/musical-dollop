import json
import plistlib


def json_serializable(o):
    return str(o)

def parse_file(file):
    playlist = None
    with open(file, 'rb') as itunes_playlist_file:
        playlist = itunes_playlist_file.read()
        playlist = plistlib.loads(playlist)
    return playlist
