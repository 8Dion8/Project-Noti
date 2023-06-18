import sqlite3 as sql
import os
import re
from datetime import datetime
from datetime import timedelta
import configparser
config = configparser.ConfigParser()


HOME = os.environ['HOME'] + "/"
CONFIG = HOME + ".config/project-noti/"
MAIN_TABLE_PATH = CONFIG + "master.sqlite3"
CONFIG_PATH = CONFIG + "conf.ini"

config.read(CONFIG_PATH)


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


def grab_rows(
        table: str,
        dbpath: str,
        start_timestamp="2022-12-31 23:59:59.999999",
        end_timestamp="2052-01-01 00:00:00.000000",
        db_time_column="timestamp") -> list:

    connection = sql.connect(dbpath)
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM {table} WHERE {db_time_column} BETWEEN '{start_timestamp}' AND '{end_timestamp}';")
    rows = cursor.fetchall()
    connection.close()
    return [list(i) for i in rows]


def create_table(table: str) -> None:
    query = f'''
    CREATE TABLE IF NOT EXISTS {table} (
        data TEXT,
        tags TEXT,
        timestamp DATETIME,
        duration REAL,
        confidence REAL
    );
    '''
    cursor.execute(query)


def parse_timestamp(timestamp: str, zonecor: int = 0) -> datetime:
    try:
        timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f+00:00")
    except:
        try:
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S+00:00")
        except:
            timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S.%f")

    return timestamp + timedelta(hours=zonecor)


def format_timestamp(timestamp: datetime, simple: bool = False) -> str:
    if simple:
        return timestamp.strftime("%Y-%m-%d")
    else:
        return timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")+"+00:00"


def get_config(section: str, value="") -> str:
    if value:
        return config[section][value]
    else:
        return config[section].items()


def set_config(section: str, value: str, var: str) -> None:
    config[section][value] = var
    with open(CONFIG_PATH, "w") as cf:
        config.write(cf)


def format_for_apexcharts(data) -> dict:
    formatted = {
        "list": []
    }
    epoch = datetime.utcfromtimestamp(0)
    names = []
    for row in data:
        start = (parse_timestamp(row[2]) - epoch).total_seconds()*1000
        if row[0] in names:
            ind = names.index(row[0])
            formatted["list"][ind]["data"].append(
                {
                    "x": row[1],
                    "y": [
                        start,
                        start + (row[3]*1000)
                    ],
                    "fillColor": get_config("colors", row[1])

                }
            )
        else:
            names.append(row[0])
            formatted["list"].append(
                {
                    "name": row[0],
                    "data": [{
                        "x": row[1],
                        "y": [
                            start,
                            start + (row[3]*1000)
                        ],
                        "fillColor": get_config("colors", row[1])
                    }]
                }
            )

    return formatted


if __name__ == "__main__":
    today = datetime.now()
    start_timestamp = format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )-timedelta(microseconds=1))
    end_timestamp = format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )+timedelta(days=1))
    AW_DATA = grab_rows(
        "aw",
        MAIN_TABLE_PATH,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )

    print(format_for_apexcharts(AW_DATA))
