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


# afk data loop
afk_periods = []
for event in tqdm(AW_DATA):
    aw_watcher_num = event[1]
    if aw_watcher_num != 2: continue
    timestamp = event[2]
    duration = event[3]
    data = event[4]
    if "not-afk" in data:
        afk = False
    else:
        afk = True

    if not afk:
        start = noti.parse_timestamp(timestamp)
        end = start + timedelta(seconds=duration)

        if len(afk_periods) and afk_periods[-1][1] >= start and afk_periods[-1][1] < end:
            afk_periods[-1][1] = end
        else:
            afk_periods.append([start, end])

print()
    