"""Test the mapping functionality. Uses an sqlite database in place of postgres."""
import logging

import pytest

from data_importer import Importer

logger = logging.getLogger("data-importer")


@pytest.mark.anyio
def test_generate_mapping() -> None:
    rows = Importer("./test_mapping.json").process()
    logger.info(rows)
