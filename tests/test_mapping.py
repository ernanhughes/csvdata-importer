"""Test the mapping functionality. Uses an sqlite database in place of postgres."""
import pytest

data = {
    "CSV_PATH": "test",
    "DATABASE_URL": "sqlite:./test-data-importer.db",
    "TARGET_TABLE": "test",
    "MAPPING": [
        {
            "name": "Zaphod Beeblebrox",
            "species": "Betelgeusian",
            "eval": ""
        },

    ]
}


@pytest.mark.anyio
def test_simple_config() -> None:
    res = "./test.json"
    print(res)
