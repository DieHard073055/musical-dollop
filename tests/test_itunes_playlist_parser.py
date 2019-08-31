import itunes_playlist_parser
import pytest
import json


def json_serializable(o):
    return str(o)

def read_results_file(results_file):
    with open(results_file, "r") as rfile:
        return rfile.read()

@pytest.mark.parametrize("itunes_playlist_files", [
    ("./data/maya.xml"),
    ('./data/mymusic.xml'),
    ('./data/pl1.xml'), 
    ('./data/pl2.xml')
])
def test_parse_file(itunes_playlist_files):
    items = itunes_playlist_parser.parse_file(itunes_playlist_files)
    assert read_results_file(f"{itunes_playlist_files}_parsed_results.txt") == json.dumps(items, indent=4, default=json_serializable)

