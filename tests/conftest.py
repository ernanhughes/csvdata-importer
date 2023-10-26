import logging
import os

import pytest

logger = logging.getLogger(__name__)

CREATE_SQL = """
    -- quote table
    CREATE TABLE IF NOT EXISTS quote (
        id integer PRIMARY KEY,
        name text,
        source text,
        date text,
        open text,
        high text,
        low text,
        close text,
        adj_close text,
        volume text
    );
"""

__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))


@pytest.fixture
def db_url(db_path):
    path = f'sqlite:///{db_path}'
    return path


@pytest.fixture
def db_path():
    return os.path.join(__location__, "test.db")


@pytest.fixture
def test_mapping():
    return os.path.join(__location__, "test_mapping.json")


@pytest.fixture
def test_csv():
    return os.path.join(__location__, "test.csv")


@pytest.fixture
def generated_mapping():
    return os.path.join(__location__, "generated_mapping.json")
