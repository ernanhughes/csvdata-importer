"""Class wrapper around a mapping file."""
import json
import logging
from enum import Enum
from os import path
from typing import Any, Dict, List, Literal
from urllib.parse import urlparse

import sqlalchemy
from sqlalchemy import inspect

logger = logging.getLogger("data-importer")

FILE_PATH = "FILE_PATH"
DATABASE_URL = "DATABASE_URL"
TARGET_TABLE = "TARGET_TABLE"
COLUMN_MAPPING = "COLUMN_MAPPING"
REQUIRED = "REQUIRED"
COLUMN_NAME = "COLUMN_NAME"
FILE_COLUMN_NAME = "FILE_COLUMN_NAME"
CONSTANT = "CONSTANT"
EVAL = "EVAL"
MAPPING_TYPE = "MAPPING_TYPE"
CONSTANT_VALUE = "CONSTANT_VALUE"
# The value from the file is transferred directly to the table
DIRECT = "DIRECT"
# What action is take if the target table exists
IF_EXISTS = "IF_EXISTS"


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

    @property
    def column_name(self): return self[COLUMN_NAME]

    @property
    def file_column_name(self): return self[FILE_COLUMN_NAME]

    @property
    def required(self): return self[REQUIRED]

    @property
    def mapping_type(self): return self[MAPPING_TYPE]

    @property
    def constant_value(self): return self[CONSTANT_VALUE]

    def __init__(self, config: Dict[str, Any]) -> None:
        super().__init__(config)
        # default to the mapped database column name
        self[FILE_COLUMN_NAME] = config.get(FILE_COLUMN_NAME, self[COLUMN_NAME])
        self[REQUIRED] = config.get(REQUIRED, "True")
        self[MAPPING_TYPE] = config.get(MAPPING_TYPE, DIRECT)
        self[CONSTANT_VALUE] = config.get(CONSTANT_VALUE, "")

    @staticmethod
    def parse(column) -> Dict[str, Any]:
        return {
            COLUMN_NAME: column['name'],
            FILE_COLUMN_NAME: column['name'],
            EVAL: "",
            MAPPING_TYPE: DIRECT,
            REQUIRED: "True" if column['nullable'] else "False",
            CONSTANT_VALUE: "",
            "type": str(column['type']),
            "nullable": column['nullable'],
            "autoincrement": column['autoincrement'],
            "comment": column['comment'],
            "default": column['default']
        }


class Mapping(Dict[str, Any]):
    """Class wrapper around a configuration file."""

    @property
    def file_path(self) -> str:
        return self[FILE_PATH]

    @property
    def target_table(self) -> str:
        return self[TARGET_TABLE]

    @property
    def if_exists(self) -> Literal["fail", "replace", "append"]:
        return self[IF_EXISTS]

    @property
    def column_mappings(self) -> List[ColumnMapping]:
        return [ColumnMapping(i) for i in self[COLUMN_MAPPING]]

    def __init__(self, config: Dict[str, Any]) -> None:
        """Initialize the config."""
        super().__init__(config)
        self[IF_EXISTS] = config.get(IF_EXISTS, "append")

    def __str__(self) -> str:
        """Return the config as a string."""
        return json.dumps(self, indent=4)

    def is_postgres(self) -> bool:
        return str(self[DATABASE_URL]).__contains__("postgres")

    def get_engine_connection_string(self) -> str:
        if self.is_postgres():
            url = urlparse(self[DATABASE_URL])
            database = url.path[1:]
            logger.info("Engine connection string: postgresql+psycopg2://%s:****@%s:%s/%s",
                        url.username, url.hostname, url.port, database)
            return f'postgresql+psycopg2://{url.username}:{url.password}@{url.hostname}:{url.port}/{database}'
        else:
            return ""

    @staticmethod
    def generate_mapping(dsn: str, table_name: str) -> str:
        """Generate a mapping file for the data importer."""
        config = Mapping({DATABASE_URL: dsn, TARGET_TABLE: table_name})
        engine = sqlalchemy.create_engine(config.get_engine_connection_string())
        inspector = inspect(engine)
        columns_table = inspector.get_columns(table_name)
        cols = []
        for column in columns_table:
            cols.append(ColumnMapping.parse(column))
        config[COLUMN_MAPPING] = cols
        return str(config)


def load_config(config: str) -> Mapping:
    """Import a file using the config file and return the result."""
    if path.isfile(config):
        logger.info("loading config %s as file", config)
        with open(config, encoding="utf-8") as f:
            return Mapping(json.load(f))
    else:
        logger.info("loading config %s as text", config)
        return Mapping(json.loads(config))
