"""Test the mapping functionality. Uses an sqlite database in place of postgres."""
import json
import logging

from data_importer import Mapping

logger = logging.getLogger("data-importer")


def test_generate_mapping(test_csv, generated_mapping) -> None:
    db_url = "postgresql://stock_prediction:stock_prediction@localhost:5432/stock_prediction"
    mapping_text = Mapping.generate_mapping(db_url, 'quote')
    mapping = Mapping(json.loads(mapping_text))
    mapping["FILE_PATH"] = test_csv
    print("Opening: %s", generated_mapping)
    mapping_file = open(generated_mapping, "w")
    n = mapping_file.write(str(mapping))
    mapping_file.close()
    logger.info("Created %d", n)
