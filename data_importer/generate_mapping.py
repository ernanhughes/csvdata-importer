"""This module is used to generate the mapping file for the data importer."""
import json
from urllib.parse import urlparse
import psycopg2



def generate_mapping(dsn: str, table_name:str) -> str:
    """Generate a mapping file for the data importer."""
    result = urlparse(dsn)
    username = result.username
    password = result.password
    database = result.path[1:]
    hostname = result.hostname
    port = result.port
    mapping = []
    with psycopg2.connect(
        dbname=database,
        user=username,
        password=password,
        host=hostname,
        port=port,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name} LIMIT 1")
            colnames = [desc[0] for desc in cur.description]
            for colname in colnames:
                mapping.append(
                    {
                        "name": colname,
                        "species": "Betelgeusian",
                        "eval": "",
                    }
                )
    return json.dumps(
        {
            "CSV_PATH": "test",
            "DATABASE_URL": dsn,
            "TARGET_TABLE": table_name,
            "MAPPING": mapping,
        },
        indent=4,
    )
