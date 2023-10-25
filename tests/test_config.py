"""Test the mapping functionality. Uses a sqlite database in place of postgres."""
import json
import logging

import pytest

from data_importer import Mapping

FILE_PATH = "FILE_PATH"
DATABASE_URL = "DATABASE_URL"
TARGET_TABLE = "TARGET_TABLE"
COLUMN_MAPPING = "COLUMN_MAPPING"

logger = logging.getLogger("data-importer")


@pytest.mark.anyio
def test_load_config_file() -> None:
    """Test opening a json file as a config dictionary."""
    with open("./test_mapping.json", encoding="utf-8") as f:
        d = json.load(f)
        c = Mapping(d)
        assert d[FILE_PATH] == c.file_path
        assert d[TARGET_TABLE] == c.target_table
        assert len(d[COLUMN_MAPPING]) == len(c[COLUMN_MAPPING])
        logger.info("Config Object:\n %s", str(c))
        logger.info("Dictionary Object:\n %s", str(d))
        logger.info("Dictionaries are equal: %d", compare_dicts(c, d))
        assert compare_dicts(c, d)


@pytest.mark.anyio
def test_load_config_string() -> None:
    """Test opening a json string as a config dictionary."""
    with open("./test_mapping.json", encoding="utf-8") as f:
        d = json.loads(f.read())
        c = Mapping(d)
        assert d[FILE_PATH] == c.file_path
        assert d[TARGET_TABLE] == c.target_table
        logger.info("Length comparison: %d", len(d[COLUMN_MAPPING]) == len(c[COLUMN_MAPPING]))
        logger.info("Config Object:\n %s", str(c))
        logger.info("Dictionary Object:\n %s", str(d))
        logger.info("Dictionaries are equal: %d", compare_dicts(c, d))
        assert compare_dicts(c, d)


def compare_dicts(dict1, dict2):
    return all(dict1.get(key) == dict2.get(key) for key in dict1)
