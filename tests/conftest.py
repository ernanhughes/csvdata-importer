import logging
import sqlite3
import pytest

logger = logging.getLogger(__name__)


CREATE_SQL = """
    -- projects table
    CREATE TABLE IF NOT EXISTS project (
        id integer PRIMARY KEY,
        name text NOT NULL,
        begin_date text,
        end_date text
    );
    
    -- tasks table
    CREATE TABLE IF NOT EXISTS task (
        id integer PRIMARY KEY,
        name text NOT NULL,
        priority integer,
        project_id integer NOT NULL,
        status_id integer NOT NULL,
        begin_date text NOT NULL,
        end_date text NOT NULL,
        FOREIGN KEY (project_id) REFERENCES projects (id)
    );
    
    CREATE TABLE IF NOT EXISTS task_data (
        id integer PRIMARY KEY,
        id integer,
        year INT, 
        sum DOUBLE
        FOREIGN KEY (task_id) REFERENCES tass (id)
    );
"""


@pytest.fixture(scope="session")
def client():
    con = sqlite3.connect('data.db')
    curs = con.cursor()
    curs.execute(CREATE_SQL)
    curs.execute("""CREATE TABLE IF NOT EXISTS data(year INT, sum DOUBLE);""")
    vals = [('2020', '8400.00'), ('2020', '8500.00'),
            ('2020', '5000.00'), ('2020', '5051.45'),
            ('2021', '9928.54'), ('2021', '9302.00'),
            ('2021', '4913.80'), ('2021', '5100.00'),
            ('2022', '4567.89'), ('2022', '4120.90'),
            ('2022', '5908.09'), ('2023', '6700.89')]
    curs.executemany("INSERT INTO data VALUES(?, ?);", vals)
    con.commit()
    curs.execute("SELECT * FROM data;")
    result = curs.fetchall()
    print(result)
