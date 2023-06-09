import sys
import os
import re
from datetime import datetime, time
from datetime import timedelta
from tqdm import tqdm
from unicodedata import normalize

from sqlite3 import Warning

import importlib.machinery
import importlib.util
loader = importlib.machinery.SourceFileLoader(
    "noti", sys.path[0] + "/../noti-bibli/noti.py")
spec = importlib.util.spec_from_loader("noti", loader)
noti = importlib.util.module_from_spec(spec)
loader.exec_module(noti)


def main():

    AW_DB_PATH = os.environ['HOME'] + \
        "/.local/share/activitywatch/aw-server/peewee-sqlite.v2.db"
    AW_DB_WIN_PATH = "/win_hdd/Users/Dion/AppData/Local/activitywatch/activitywatch/aw-server/peewee-sqlite.v2.db"
    
    AW_WIN_DATA = noti.grab_rows("eventmodel", AW_DB_WIN_PATH)
    for row in AW_WIN_DATA:
        row[2] = noti.format_timestamp(noti.parse_timestamp(row[2], 3))

    AW_DATA = noti.grab_rows("eventmodel", AW_DB_PATH)
    AW_DATA.extend(AW_WIN_DATA)
    AW_DATA = sorted(AW_DATA, key=lambda k: k[2])

    noti.create_table("aw")

    last_updated = noti.parse_timestamp(noti.get_config("aw", "last_updated"))
    print("last updated:", last_updated)
    total_data = []

    category_regex = noti.get_config("regex")

    never_afk_reg = re.compile(noti.get_config("aw", "never_afk_reg"))

    # afk data loop
    afk_periods = []
    for event in tqdm(AW_DATA):
        aw_watcher_num = event[1]
        if aw_watcher_num not in [2, 13]:
            continue
        timestamp = event[2]
        start = noti.parse_timestamp(timestamp, 3)
        if start < last_updated:
            continue
        duration = event[3]
        data = event[4]
        if "not" in data:
            end = start + timedelta(seconds=duration)

            if len(afk_periods) and afk_periods[-1][1] >= start and afk_periods[-1][1] < end:
                afk_periods[-1][1] = end
            else:
                afk_periods.append([start, end])


    if not len(afk_periods):
        afk_periods.append([last_updated, datetime.now()])

    for event in tqdm(AW_DATA):
        aw_watcher_num = event[1]
        if aw_watcher_num not in [1, 12]:
            continue

        duration = event[3]
        if not duration:
            continue

        timestamp = event[2]
        event_start = noti.parse_timestamp(timestamp, 3)
        if event_start < last_updated:
            continue
        event_end = event_start + timedelta(seconds=duration)

        data = eval(event[4])["app"]

        if data == "firefox":
            data += ": " + eval(event[4])["title"]

            data = data.replace("'", "")
            data = data.encode('utf-8','ignore').decode("utf-8")

        if never_afk_reg.search(data.lower()):
            total_data.append([data, event_start, duration])
            continue

        for afk_start, afk_end in afk_periods:
            if afk_start <= event_start < afk_end:
                true_end = min(afk_end, event_end)
                true_duration = true_end - event_start
                true_duration = true_duration.total_seconds()
                
                if len(total_data):
                    last_event = total_data[-1]
                    
                    if event_start - last_event[1] - timedelta(seconds=last_event[2]) < timedelta(seconds=10):
                        if last_event[0] == data:
                            dif = true_end - \
                                (last_event[1]+timedelta(seconds=last_event[2]))
                            total_data[-1][2] = last_event[2] + dif.total_seconds()
                            continue
                        else:
                            event_start = last_event[1] + timedelta(seconds=last_event[2]) + timedelta(microseconds=1) 

                total_data.append([data, event_start, true_duration])
                break


    for data, timestamp, duration in tqdm(total_data):
        category_set = False
        for (key, val) in category_regex:
            if re.search(val, data.lower(), re.IGNORECASE):
                try:
                    noti.write(
                        data,
                        timestamp,
                        duration,
                        "aw",
                        tags=key
                    )
                except Warning:
                    print(data)
                    exit(1)
                category_set = True
                break
        if not category_set:
            try:
                noti.write(
                    data,
                    timestamp,
                    duration,
                    "aw",
                    tags="uncategorised"
                )
            except Warning:
                print(data)
                exit(1)
    try:
        noti.set_config(
            "aw",
            "last_updated",
            noti.format_timestamp(total_data[-1][1])
        )
    except: pass


if __name__ == "__main__":
    main()