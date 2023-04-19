import sqlite3 as sql
import os
import re
from datetime import datetime
from datetime import timedelta

MAIN_TABLE_PATH = "/home/dion/.config/project-noti/master.sqlite3"

# MAIN DATA STRUCTURE
# | DATA | TAGS | TIMESTAMP | DURATION | CONFIDENCE |
# +------+------+-----------+----------+------------+
# | TEXT | TEXT | TIMESTAMP |   REAL   |    REAL    |
#          YYYY-MM-DD hh:mm:ss.uuuuu

connection = sql.connect(MAIN_TABLE_PATH, isolation_level=None)
cursor = connection.cursor()

def write(data: str, timestamp: datetime, duration: float, table: str, confidence=1.0, tags="") -> None:
    timestamp = timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")
    query = f"INSERT INTO {table} VALUES ('{data}', '{tags}', '{timestamp}', {duration}, {confidence});"
    
    cursor.execute(query)

def reset_table(table: str) -> None:
    cursor.execute(f"DROP TABLE {table};")

def grab_rows(table: str, dbpath: str) -> list:
    connection = sql.connect(dbpath)
    cursor = connection.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    connection.close()
    return rows

def create_table(table: str) -> None:
    query = f'''
    CREATE TABLE IF NOT EXISTS {table} (
        data TEXT,
        tags TEXT,
        time DATETIME,
        duration REAL,
        confidence REAL
    );
    '''
    cursor.execute(query)

def parse_timestamp(timestamp: str) -> datetime:
    try:
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f+00:00")
    except:
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S+00:00")
    
    return timestamp

def format_timestamp(timestamp: datetime) -> str:
    return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")+"+00:00"