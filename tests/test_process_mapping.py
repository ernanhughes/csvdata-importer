"""Test the mapping functionality. Uses an sqlite database in place of postgres."""
import json
import logging

from data_importer import Importer, Mapping, load_config

logger = logging.getLogger("data-importer")


def test_generate_mapping(test_mapping, test_csv) -> None:
    f = open(test_mapping, encoding='utf-8')
    mapping = Mapping(json.load(f))
    mapping["FILE_PATH"] = test_csv
    rows = Importer(str(mapping)).process()
    logger.info(rows)


def test_load_config(test_mapping) -> None:
    load_config(test_mapping)
