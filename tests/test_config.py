"""Test the mapping functionality. Uses a sqlite database in place of postgres."""
import json

import pytest

from data_importer import ConfigDict

FILE_PATH = "FILE_PATH"
DATABASE_URL = "DATABASE_URL"
TARGET_TABLE = "TARGET_TABLE"
MAPPING = "MAPPING"


@pytest.mark.anyio
def test_load_config_file() -> None:
    """Test opening a json file as a config dictionary."""
    with open("./test.json", encoding="utf-8") as f:
        d = json.load(f)
        c = ConfigDict(d)
        assert d[FILE_PATH] == c.file_path
        assert d[TARGET_TABLE] == c.target_table
        assert len(d[MAPPING]) == len(c.column_mappings)
        print(f'Config Object:\n {str(c)}')
        print(f'Dictionary Object:\n {str(d)}')
        print(f'Dictionaries are equal: {compare_dicts(c, d)}')
        assert compare_dicts(c, d)


@pytest.mark.anyio
def test_load_config_string() -> None:
    """Test opening a json string as a config dictionary."""
    with open("./test.json", encoding="utf-8") as f:
        d = json.loads(f.read())
        c = ConfigDict(d)
        assert d[FILE_PATH] == c.file_path
        assert d[TARGET_TABLE] == c.target_table
        assert len(d[MAPPING]) == len(c.column_mappings)
        print(f'Config Object:\n {str(c)}')
        print(f'Dictionary Object:\n {str(d)}')
        print(f'Dictionaries are equal: {compare_dicts(c, d)}')
        assert compare_dicts(c, d)


def compare_dicts(dict1, dict2):
    return all(dict1.get(key) == dict2.get(key) for key in dict1)
