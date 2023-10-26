"""Test the ColumnMappingType enum functionality."""
import pytest

from data_importer import ColumnMappingType


def test_mapping_type() -> None:
    assert ColumnMappingType.parse("DIRECT") == ColumnMappingType.DIRECT


def test_mapping_type_fail() -> None:
    with pytest.raises(ValueError):
        ColumnMappingType.parse("WILL NOT MAP")
