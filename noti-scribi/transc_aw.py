import sys
import os
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm

import importlib.machinery
import importlib.util
loader = importlib.machinery.SourceFileLoader(
    "noti", sys.path[0] + "/../noti-bibli/noti.py")
spec = importlib.util.spec_from_loader("noti", loader)
noti = importlib.util.module_from_spec(spec)
loader.exec_module(noti)


AW_DB_PATH = os.environ['HOME'] + \
    "/.local/share/activitywatch/aw-server/peewee-sqlite.v2.db"
AW_DATA = noti.grab_rows("eventmodel", AW_DB_PATH)
AW_DATA = sorted(AW_DATA, key=lambda k: k[2])

noti.create_table("aw")

last_updated = noti.parse_timestamp(noti.get_config("aw", "last_updated"))
print("last updated:", last_updated)
total_data = []

# afk data loop
afk_periods = []
for event in tqdm(AW_DATA):
    aw_watcher_num = event[1]
    if aw_watcher_num != 2:
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
    if aw_watcher_num != 1:
        continue

    duration = event[3]
    if not duration:
        continue

    timestamp = event[2]
    event_start = noti.parse_timestamp(timestamp, 3)
    if event_start < last_updated:
        continue
    event_end = event_start + timedelta(seconds=duration)

    for afk_start, afk_end in afk_periods:
        if afk_start <= event_start < afk_end:
            true_end = min(afk_end, event_end)
            true_duration = true_end - event_start
            true_duration = true_duration.total_seconds()
            data = eval(event[4])["app"]

            if len(total_data):
                last_event = total_data[-1]
                if last_event[0] == data and event_start - last_event[1] - timedelta(seconds=last_event[2]) < timedelta(seconds=10):
                    dif = true_end - \
                        (last_event[1]+timedelta(seconds=last_event[2]))
                    total_data[-1][2] = last_event[2] + dif.total_seconds()
                    continue

            total_data.append([data, event_start, true_duration])
            break

for data, timestamp, duration in tqdm(total_data):
    noti.write(
        data,
        timestamp,
        duration,
        "aw"
    )
try:
    noti.set_config(
        "aw",
        "last_updated",
        noti.format_timestamp(total_data[-1][1])
    )
except: pass