"""Test the mapping functionality. Uses an sqlite database in place of postgres."""
import pytest

from data_importer import Importer


@pytest.mark.anyio
def test_generate_mapping() -> None:
    rows = Importer("./test_mapping.json").process()
    print(rows)
