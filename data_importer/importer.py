"""Module providing a way to import data to data tables."""
import logging.config

import pandas as pd
from sqlalchemy import create_engine

from .mapping import Mapping, load_config, ColumnMappingType

logger = logging.getLogger("data-importer")


class Importer:
    """ Class for importing data to a database table based upon the mapping file"""
    config: Mapping

    def __init__(self, config: str):
        self.config = load_config(config)

    def process(self) -> int:
        """Process the config and return the result.
           Will handle string json and a file path.
           Note that if_exists will change behaviour of operation based upon data existing in the target table.
           Will return teh number of rows inserted ot the target table."""
        file_path = self.config.file_path
        logger.info("Loading file: %s", file_path)
        df = pd.read_csv(file_path)
        engine = create_engine(self.config.get_engine_connection_string())
        mapped_columns = []
        for col in self.config.column_mappings:
            mapped_columns.append(col.column_name)
            if col.file_column_name in df.columns:
                if col.file_column_name != col.column_name:
                    logger.info("Renaming column %s to column Name: %s.",
                                col.file_column_name, col.column_name)
                    df = df.rename(columns={col.file_column_name: col.column_name})
            if col.mapping_type == ColumnMappingType.CONSTANT.value:
                logger.info("Assigning column: %s to constant value %s as it is configured to be constant",
                            col.column_name, col.column_value)
                data = {col.column_name: col.column_value}
                df = df.assign(**data)
            elif col.mapping_type == ColumnMappingType.EVALUATED.value:
                logger.info("Evaluating column: %s: (%s) as it is configured to be evaluated",
                            col.column_name, col.column_value)
                df[col.column_name] = df.eval(col.column_value)
        for col in df.columns:
            if col not in mapped_columns:
                logger.info("Dropping column %s because it is not mapped in list [%s]",
                            col, mapped_columns)
                df = df.drop(columns=[col])
        logger.info("Inserting data to: %s", self.config.target_table)
        sql_insert = df.to_sql(self.config.target_table, engine, if_exists=self.config.if_exists, index=False)
        return sql_insert
