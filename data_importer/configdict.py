"""Class wrapper around a configuration file."""
import json
import logging
from enum import Enum
from os import path
from typing import Any, Dict, List
from urllib.parse import urlparse

import psycopg2

logger = logging.getLogger(__file__)

FILE_PATH = "FILE_PATH"
DATABASE_URL = "DATABASE_URL"
TARGET_TABLE = "TARGET_TABLE"
MAPPING = "MAPPING"
REQUIRED = "REQUIRED"
COLUMN_NAME = "COLUMN_NAME"
FILE_COLUMN_NAME = "FILE_COLUMN_NAME"


class ColumnMappingType(Enum):
    DIRECT = 1  # When we are mapping directly from one field to another
    EVALUATED = 2  # When we are performing an evaluation to determine final result
    CONSTANT = 3  # When we are using a constant for a field value

    @staticmethod
    def parse(value: str):
        for enum_member in ColumnMappingType:
            if enum_member.name == value:
                return enum_member
        raise ValueError(f"'{value}' is not a valid value for ColumnMappingType enumeration.")


class ColumnMapping(Dict[str, Any]):
    """How we map and process each column from data in a file."""
    column_name: str
    file_column_name: str
    required: bool = False
    type: ColumnMappingType = ColumnMappingType.DIRECT

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        self.column_name = config["COLUMN_NAME"]
        self.file_column_name = config.get("FILE_COLUMN_NAME", self.column_name)
        self.required = config.get("REQUIRED", "True")
        self.TYPE = config.get("TYPE", "DIRECT")
        self.type = ColumnMappingType.parse(str(self.TYPE))


class ConfigDict(Dict[str, Any]):
    """Class wrapper around a configuration file."""
    database: str
    username: str
    password: str
    hostname: str
    port: int
    _file_path: str
    target_table: str
    column_mappings: List[ColumnMapping] = []

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the config."""
        super().__init__(config)
        self.file_path = config[FILE_PATH]
        self.process_db_url(config[DATABASE_URL])
        self.target_table = config[TARGET_TABLE]
        for mapping in config[MAPPING]:
            print(f'Adding mapping: {str(mapping)} ')
            m = ColumnMapping(mapping)
            self.column_mappings.append(m)

    def __str__(self) -> str:
        """Return the config as a string."""
        return json.dumps(self, indent=4)

    @property
    def file_path(self):
        return self._file_path

    @file_path.setter
    def file_path(self, new_value):
        self[FILE_PATH] = new_value
        self._file_path = new_value

    def add_column_mapping(self, column_mapping: Dict[str, Any]) -> None:
        self.column_mappings.append(ColumnMapping(column_mapping))
        self[MAPPING] = []
        for column_mapping in self.column_mappings:
            self[MAPPING].append(column_mapping)
        print(str(self))

    def process_db_url(self, db_url: str) -> None:
        """Import a file using the config file and return the result."""
        result = urlparse(db_url)
        self.username = result.username
        self.password = result.password
        self.database = result.path[1:]
        self.hostname = result.hostname
        self.port = result.port

    def is_postgres(self) -> bool:
        return str(self[DATABASE_URL]).startswith("postgres")

    @staticmethod
    def generate_mapping(dsn: str, table_name: str) -> str:
        """Generate a mapping file for the data importer."""
        config = ConfigDict({DATABASE_URL: dsn, TARGET_TABLE: table_name,
                             FILE_PATH: "",
                             MAPPING: []})
        result = urlparse(dsn)
        config.username = result.username
        config.password = result.password
        config.database = result.path[1:]
        config.hostname = result.hostname
        config.port = result.port
        with psycopg2.connect(
                dbname=config.database,
                user=config.username,
                password=config.password,
                host=config.hostname,
                port=config.port,
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"SELECT * FROM {table_name} WHERE FALSE")
                col_names = [desc[0] for desc in cur.description]
                for col_name in col_names:
                    config.add_column_mapping(ColumnMapping({
                        COLUMN_NAME: col_name,
                        FILE_COLUMN_NAME: col_name,
                        "eval": "",
                        REQUIRED: "True"
                    }))
        return str(config)


def load_config(config: str) -> ConfigDict:
    """Import a file using the config file and return the result."""
    if path.isfile(config):
        with open(config, encoding="utf-8") as f:
            return ConfigDict(json.load(f))
    else:
        return ConfigDict(json.loads(config))
