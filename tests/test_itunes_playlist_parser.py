
import itunes_playlist_parser
import pytest
import json
import os
from pathlib import Path

""" TODO:
- [x] find duplicates in the playlist
- [x] find common tracks across a list of given playlist
- [x] plot common statistics
"""
TEST_DIR_NAME='data'
TEST_DIR_PATH=Path(os.path.join(os.path.dirname(__file__), TEST_DIR_NAME))

def json_serializable(o):
    return str(o)

def read_results_file(results_file):
    with open(results_file, "r") as rfile:
        return rfile.read()

@pytest.mark.parametrize("playlist_file", [
        ('maya.xml'),
        ('mymusic.xml'),
        ('pl1.xml'),
        ('pl2.xml')
])
def test_parse_file(playlist_file):
    items = itunes_playlist_parser.parse_file(os.path.join(TEST_DIR_PATH, playlist_file))
    file_path = os.path.join(TEST_DIR_PATH, f"{playlist_file}_parsed_results.txt")
    assert read_results_file(file_path) == json.dumps(items, indent=4, default=json_serializable)

@pytest.mark.parametrize("playlist_file, nof_duplicates", [
        ('maya.xml', 0),
        ('mymusic.xml', 238),
        ('pl1.xml', 1),
        ('pl2.xml', 3)
])
def test_duplicates_in_playlist(playlist_file, nof_duplicates):
    items = itunes_playlist_parser.parse_file(os.path.join(TEST_DIR_PATH, playlist_file))
    tracks = items["Tracks"]

    # calculate duplicates
    duplicates = itunes_playlist_parser.get_duplicate_tracks(tracks)
    assert len(duplicates) == nof_duplicates, "should have the exact amount of duplicates we provided"

@pytest.mark.parametrize("playlist_file_1, playlist_file_2, expected_nof_common_tracks",[
        ('maya.xml', 'mymusic.xml', 67),
        ('pl1.xml', 'pl2.xml', 15)
])
def test_find_common_tracks_across_playlists(playlist_file_1, playlist_file_2, expected_nof_common_tracks):
   playlist_1 = itunes_playlist_parser.parse_file(os.path.join(TEST_DIR_PATH, playlist_file_1))["Tracks"]
   playlist_2 = itunes_playlist_parser.parse_file(os.path.join(TEST_DIR_PATH, playlist_file_2))["Tracks"]

   common_tracks = itunes_playlist_parser.find_common_tracks(playlist_1, playlist_2)

   assert (
           len(common_tracks) == expected_nof_common_tracks
    ), "should have the expected common tracks if all the commons tracks were found"

@pytest.mark.parametrize("playlist_file", [
        ('maya.xml'),
        ('mymusic.xml'),
        ('pl1.xml'),
        ('pl2.xml')
])
def test_plot_stats(playlist_file):
    tracks = itunes_playlist_parser.parse_file(os.path.join(TEST_DIR_PATH, playlist_file))["Tracks"]
    itunes_playlist_parser.plot_statistics(tracks)
