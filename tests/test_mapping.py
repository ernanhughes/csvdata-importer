import pytest

from data_importer import import_file

data = {
    "CSV_PATH": "test",
    "DATABASE_URL": "test",
    "TARGET_TABLE": "test",
    "MAPPING": {
        "name": "Zaphod Beeblebrox",
        "species": "Betelgeusian",
        "eval": ""
    }
}


@pytest.mark.anyio
def test_simple_config() -> None:
    res = import_file.import_file("./test.json")
    print(res)
