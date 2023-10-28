"""Test the mapping functionality. Uses a sqlite database in place of postgres."""
import json

from csvdata_importer import Mapping, load_mapping


def test_load_mapping_as_json_file(test_mapping) -> None:
    """Test opening a json file as a config dictionary."""
    c = Mapping(load_mapping(test_mapping))
    with open(test_mapping, encoding="utf-8") as f:
        d = json.load(f)
        assert compare_dicts(c, d)


def test_load_mapping_as_json_string(test_mapping) -> None:
    """Test opening a json string as a config dictionary."""
    with open(test_mapping, encoding="utf-8") as f:
        d = json.loads(f.read())
        c = Mapping(d)
        assert compare_dicts(c, d)


def compare_dicts(dict1, dict2):
    """Compare two dicts for equality. Used to validate that the json got
    loaded or processed correctly."""
    return all(dict1.get(key) == dict2.get(key) for key in dict1)
