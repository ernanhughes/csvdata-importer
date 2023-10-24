"""Module providing a function printing python version."""
import json
import logging.config
from os import path
from urllib.parse import urlparse
import pandas as pd


log_file_path = path.join(path.dirname(path.abspath(__file__)), 'logging.conf')
print(f'log_file_path: {log_file_path}')
logging.config.fileConfig(log_file_path)
logger = logging.getLogger(__name__)


def import_file(config: str) -> dict:
    """Import a file using the config file and return the result."""
    if path.isfile(config):
        with open(config, encoding="utf-8") as f:
            return process(json.load(f))
    else:
        return process(json.loads(config))


def process(config: dict) -> dict:
    """Process the config and return the result. 
       Will handle string json and a file path."""
    logger.info("Processing config: %s", config)
    csv_path = config["CSV_PATH"]
    assert path.isfile(csv_path)
    logger.info("Loading csv: %s", csv_path)
    df = pd.read_csv(csv_path)
    db_url = config["DATABASE_URL"]
    result = urlparse(db_url)
    username = result.username
    logger.info("Loading csv: %s", csv_path)
    password = result.password
    logger.info("Loading csv: %s", csv_path)
    database = result.path[1:]
    logger.info("Loading csv: %s", csv_path)
    hostname = result.hostname
    logger.info("Loading csv: %s", csv_path)
    port = result.port

    target_table = config["TARGET_TABLE"]
    mapping = config["MAPPING"]
    return config

    # conn = psycopg2.connect("host=localhost dbname=postgres user=postgres")
    # cur = conn.cursor()
    # with open('user_accounts.csv', 'r') as f:
    #     # Notice that we don't need the csv module.
    #     next(f)  # Skip the header row.
    #     cur.copy_from(f, 'users', sep=',')
    #
    # conn.commit()
