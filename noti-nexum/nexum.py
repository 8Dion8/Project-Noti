import json, sys, os
from flask import Flask, jsonify
from datetime import datetime
from datetime import timedelta

import importlib.machinery
import importlib.util
loader = importlib.machinery.SourceFileLoader(
    "noti", sys.path[0] + "/../noti-bibli/noti.py")
spec = importlib.util.spec_from_loader("noti", loader)
noti = importlib.util.module_from_spec(spec)
loader.exec_module(noti)



app = Flask(__name__)


@app.route('/')
def index():
    return jsonify({
        "ping": "pong!"
    })

@app.route('/today')
def get_data_today():
    today = datetime.now()
    start_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )-timedelta(microseconds=1))
    end_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )+timedelta(days=1))
    AW_DATA = noti.grab_rows(
        "aw", 
        noti.MAIN_TABLE_PATH,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )
    return jsonify({"data":AW_DATA})



app.run()