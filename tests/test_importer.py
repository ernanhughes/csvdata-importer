"""Test the mapping functionality. Uses an sqlite database in place of postgres."""
import json
import random
import sqlite3

from data_importer import Importer, Mapping, load_mapping


def test_process_mapping(test_mapping, db_url, db_path, test_csv) -> None:
    """ Here we test the mapping as a json string"""
    target_table_name = f'quote_{random.randint(10000, 99999)}'
    rows = process_mapping(test_mapping, test_csv, db_url, target_table_name)
    assert rows == count_lines_in_file(test_csv) - 1
    assert get_count_of_rows_in_table(db_path, target_table_name) == rows


def test_generate_mapping(test_mapping, db_url, db_path, test_csv) -> None:
    """
        Here we test generating the mapping, first we generate the table in the db.
        Then compare the number of columns in the table to the number of columns generated in the mapping file
    """
    target_table_name = f'quote_{random.randint(10000, 99999)}'
    process_mapping(test_mapping, test_csv, db_url, target_table_name)
    mapping = json.loads(Mapping.generate_mapping(db_url, target_table_name))
    columns_in_table = get_number_of_columns_in_table(db_path, target_table_name)
    print_table(db_path, target_table_name)
    assert len(mapping["COLUMN_MAPPING"]) == columns_in_table


def process_mapping(mapping_file_path, file_path, database_url, target_table) -> int:
    mapping = Mapping(load_mapping(mapping_file_path))
    mapping["FILE_PATH"] = file_path
    mapping["DATABASE_URL"] = database_url
    mapping["TARGET_TABLE"] = target_table
    return Importer(str(mapping)).process()


def test_load_config(test_mapping) -> None:
    """Test loading a config file"""
    load_mapping(test_mapping)


def test_database_url(test_mapping) -> None:
    """Test processing a postgres database url"""
    mapping = Mapping(load_mapping(test_mapping))
    alchemy_url = mapping.get_engine_connection_string()
    assert (alchemy_url == mapping["DATABASE_URL"]
            .replace("postgresql", "postgresql+psycopg2"))


def count_lines_in_file(file_path: str) -> int:
    """Utility function count lines in file"""
    f = open(file_path, encoding='utf-8')
    return len(f.readlines())


def get_count_of_rows_in_table(db_path, table_name) -> int:
    query = f'select count(*) from {table_name}'
    cn = sqlite3.connect(db_path)
    cursor = cn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]
    print(row_count)
    return row_count


def get_number_of_columns_in_table(db_path, table_name) -> int:
    query = f'SELECT COUNT(*) FROM pragma_table_info(\'{table_name}\')'
    cn = sqlite3.connect(db_path)
    cursor = cn.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    row_count = result[0]
    print(row_count)
    return row_count


def print_table(db_path, table_name) -> int:
    query = f'select * from {table_name}'
    cn = sqlite3.connect(db_path)
    cursor = cn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    for row in rows:
        print(row)
    cursor.close()
    cn.close()

