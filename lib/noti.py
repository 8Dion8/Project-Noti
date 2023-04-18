import sqlite3 as sql
import os
from datetime import datetime
from datetime import timedelta

MAIN_TABLE_PATH = "$HOME/.config/project-noti"

# MAIN DATA STRUCTURE
# | DATA | TAGS | TIMESTAMP | DURATION | CONFIDENCE |
# +------+------+-----------+----------+------------+
# | TEXT | TEXT | TIMESTAMP |   REAL   |    REAL    |
#          YYYY-MM-DD hh:mm:ss.uuuuu

def write(data: str, timestamp: datetime, duration: int, table: str, confidence=1.0, tags="") -> None:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    query = f'''
        INSERT INTO {table} VALUES ("{data}", "{tags}", "{timestamp}", "{duration}", "{confidence}");
        '''
    connection = sql.connect(MAIN_TABLE_PATH)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.close()

def reset_table(table: str) -> None:
    connection = sql.connect(MAIN_TABLE_PATH)
    cursor = connection.cursor()
    cursor.execute(f"DROP TABLE {table};")
    connection.close()

def grab_rows(table: str, dbpath: str) -> list:
    connection = sql.connect(dbpath)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def create_table(table: str):
    query = f'''
    CREATE TABLE IF NOT EXISTS {table} (
        data TEXT,
        tags TEXT,
        time DATETIME,
        duration REAL,
        confidence REAL
    );
    '''
    connection = sql.connect(MAIN_TABLE_PATH)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.close()