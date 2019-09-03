import itunes_playlist_parser
import pytest
import json
import os
from pathlib import Path

""" TODO:
- [ ] find duplicates in the playlist
- [ ] find common tracks across a list of given playlist
- [ ] plot the 
"""
TEST_DIR_NAME='data'
TEST_DIR_PATH=Path(os.path.join(os.path.dirname(__file__), TEST_DIR_NAME))

def json_serializable(o):
    return str(o)

def read_results_file(results_file):
    with open(results_file, "r") as rfile:
        return rfile.read()

@pytest.mark.parametrize("itunes_playlist_files", [
    ("maya.xml"),
    ('mymusic.xml'),
    ('pl1.xml'), 
    ('pl2.xml')
])
def test_parse_file(itunes_playlist_files):
    items = itunes_playlist_parser.parse_file(os.path.join(TEST_DIR_PATH, itunes_playlist_files))
    file_path = os.path.join(TEST_DIR_PATH, f"{itunes_playlist_files}_parsed_results.txt")
    assert read_results_file(file_path) == json.dumps(items, indent=4, default=json_serializable)

def test_duplicates_in_playlist():
    raise NotImplementedError()

def test_find_common_tracks_across_playlists():
    raise NotImplementedError()

def test_plot_stats_about_playlists():
    raise NotImplementedError()

