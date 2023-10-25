"""Test the mapping functionality. Uses the sqlite database in place of postgres."""
import logging

import pytest


logger = logging.getLogger("data-importer")


@pytest.mark.anyio
def test_simple_config() -> None:
    res = "./test.json"
    logger.info(res)
