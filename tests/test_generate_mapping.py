"""Test the mapping functionality. Uses an sqlite database in place of postgres."""
import json
import logging

import pytest

from data_importer import Mapping

logger = logging.getLogger("data-importer")


@pytest.mark.anyio
def test_generate_mapping() -> None:
    db_url = "postgresql://stock_prediction:stock_prediction@localhost:5432/stock_prediction"
    mapping_text = Mapping.generate_mapping(db_url, 'quote')
    mapping = Mapping(json.loads(mapping_text))
    mapping["FILE_PATH"] = "test.csv"
    mapping_file = open("generated_mapping.json", "w")
    n = mapping_file.write(str(mapping))
    mapping_file.close()
    logger.info("Created %d", n)
