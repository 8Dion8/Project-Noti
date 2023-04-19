import sys
from datetime import datetime
from datetime import timedelta
from tqdm import tqdm

import importlib.machinery
import importlib.util
loader = importlib.machinery.SourceFileLoader("noti", sys.path[0] + "/../lib/noti.py")
spec = importlib.util.spec_from_loader("noti", loader)
noti = importlib.util.module_from_spec(spec)
loader.exec_module(noti)


AW_DB_PATH = "/home/dion/.local/share/activitywatch/aw-server/peewee-sqlite.v2.db"

noti.create_table("aw")

AW_DATA = noti.grab_rows("eventmodel", AW_DB_PATH)

AW_DATA = sorted(AW_DATA, key=lambda k: k[2])

# afk data loop
afk_periods = []
for event in tqdm(AW_DATA):
    aw_watcher_num = event[1]
    if aw_watcher_num != 2: continue
    timestamp = event[2]
    start = noti.parse_timestamp(timestamp)
    if start < datetime(2022, 12, 30):continue
    duration = event[3]
    data = event[4]
    if "not" in data:
        end = start + timedelta(seconds=duration)

        if len(afk_periods) and afk_periods[-1][1] >= start and afk_periods[-1][1] < end:
            afk_periods[-1][1] = end
        else:
            afk_periods.append([start, end])

print()

last_pair = afk_periods[0]

for event in tqdm(AW_DATA):
    aw_watcher_num = event[1]
    if aw_watcher_num != 1: continue
    

    duration = event[3]
    if not duration: continue

    timestamp = event[2]
    event_start = noti.parse_timestamp(timestamp)

    if event_start < datetime(2022, 12, 31):continue
    
    event_end = event_start + timedelta(seconds=duration)

    
    if last_pair[0] <= event_start < last_pair[1]:
        true_end = min(afk_end, event_end)
        true_duration = true_end - event_start
        true_duration = true_duration.total_seconds()
        
        data = eval(event[4])["app"]
        noti.write(
            data, 
            event_start,
            true_duration,
            "aw"
        )
        #afk_periods.pop(0)
        continue

    for afk_start, afk_end in afk_periods:
        if afk_start <= event_start < afk_end:
            true_end = min(afk_end, event_end)
            true_duration = true_end - event_start
            true_duration = true_duration.total_seconds()
            
            data = eval(event[4])["app"]
            noti.write(
                data, 
                event_start,
                true_duration,
                "aw"
            )

            last_pair = [afk_start, afk_end]

            break


