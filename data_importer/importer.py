"""Module providing a way to import data to data tables."""
import logging.config
from os import path

import psycopg2
from sqlalchemy import create_engine
from .configdict import ConfigDict, load_config
import pandas as pd

log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
print(f'log_file_path: {log_file_path}')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)


class Importer:
    """ Class for importing datat to the database based upon the config file"""
    config: ConfigDict

    def __init__(self, config: str):
        self.config = load_config(config)

    def process(self) -> int:
        """Process the config and return the result.
           Will handle string json and a file path."""
        csv_path = self.config.file_path
        logger.info("Loading csv: %s", csv_path)
        df = pd.read_csv(csv_path)
        engine = create_engine(
            f"postgresql+psycopg2://{self.config.username}:{self.config.password}@{self.config.hostname}:{self.config.port}/{self.config.database}")
        for col in self.config.column_mappings:
            if col.file_column_name in df.columns:
                if col.file_column_name != col.column_name:
                    print(f"Renaming row {col.file_column_name} to column Name: {col.column_name}, ")
                    df = df.rename(columns={col.file_column_name: col.column_name})
        sql_insert = df.to_sql(self.config.target_table, engine, if_exists='replace', index=False)
        return sql_insert

