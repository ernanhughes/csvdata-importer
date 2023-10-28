"""Test the ColumnMappingType enum functionality."""
import pytest

from csvdata_importer import ColumnMappingType


def test_mapping_type() -> None:
    assert "DIRECT" == ColumnMappingType.DIRECT.value


def test_mapping_type_fail() -> None:
    with pytest.raises(KeyError):
        return ColumnMappingType["WILL NOT MAP"].value
