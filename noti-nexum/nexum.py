import json
import sys
import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from datetime import datetime
from datetime import timedelta
import numpy as np
import importlib.machinery
import importlib.util
loader = importlib.machinery.SourceFileLoader(
    "noti", sys.path[0] + "/../noti-bibli/noti.py")
spec = importlib.util.spec_from_loader("noti", loader)
noti = importlib.util.module_from_spec(spec)
loader.exec_module(noti)


app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
@cross_origin()
def index():
    return jsonify({
        "ping": "pong!"
    })


@app.route('/day/pie')
@cross_origin()
def get_pie_today():
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
    data = noti.grab_rows(
        "aw",
        noti.MAIN_TABLE_PATH,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )

    labels = ["study", "hobby", "social", "media",
              "leisure", "waste", "uncategorised"]

    formatted = {
        "series": [{
            "data": [
                {
                    "name": "Study",
                    "y": 0
                }, {
                    "name": "Hobby",
                    "y": 0
                }, {
                    "name": "Social",
                    "y": 0
                }, {
                    "name": "Media",
                    "y": 0
                }, {
                    "name": "Leisure",
                    "y": 0
                }, {
                    "name": "Waste",
                    "y": 0
                }, {
                    "name": "Uncategorised",
                    "y": 0
                }
            ]
        }]
    }

    for row in data:
        tag = row[1]
        duration = row[3]

        tag_index = labels.index(tag)

        formatted["series"][0]["data"][tag_index]["y"] += duration

    for i in formatted["series"][0]["data"]:
        if i["y"] < 10:
            i["y"] = None
        else:
            i["y"] = round(i["y"] / 6) / 10

    return jsonify(formatted)


@app.route('/day/timeline')
@cross_origin()
def get_timeline_today():
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
    data = noti.grab_rows(
        "aw",
        noti.MAIN_TABLE_PATH,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )

    labels = ["study", "hobby", "social", "media",
              "leisure", "waste", "uncategorised"]
    colors = ["#7fbbb3", "#3f5865", "#a7c080",
              "#e69875", "#dbbc7f", "#7a8478", "#5d6b66"]

    unf = []

    epoch = datetime.utcfromtimestamp(0)

    for event in data:
        x = (noti.parse_timestamp(event[2]) - epoch).total_seconds() * 1000
        x2 = x + (event[3] * 1000)
        y = labels.index(event[1])
        unf.append({
            "x": x,
            "x2": x2,
            "y": y,
            "name": event[0],
            "color": colors[y]
        })

    return jsonify({"series": unf})

@app.route('/day/timeline/y')
@cross_origin()
def get_timeline_today_y():
    return jsonify(["Study", "Hobby", "Social", "Media", "Leisure", "Waste", "Uncategorised"])

@app.route('/day/last_columns')
@cross_origin()
def get_columns_today():

    last_n = int(request.args["n"])

    today = datetime.now()
    start_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )-timedelta(days=last_n-1))
    end_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )+timedelta(days=1))
    data = noti.grab_rows(
        "aw",
        noti.MAIN_TABLE_PATH,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )

    labels = ["study", "hobby", "social", "media",
              "leisure", "waste", "uncategorised"]

    formatted = {
        "series": [
            {
                "name": "study",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "hobby",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "social",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "media",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "leisure",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "waste",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "uncategorised",
                "data": list(np.zeros(last_n)),
                "type": "column"
            }]
    }

    for row in data:
        tag_index = labels.index(row[1])
        timestamp = noti.parse_timestamp(row[2])
        day_index = (timestamp - noti.parse_timestamp(start_timestamp)).days
        formatted["series"][tag_index]["data"][day_index] += row[3]

    for i in range(len(formatted["series"])):
        for j in range(last_n):
            formatted["series"][i]["data"][j] = round(
                formatted["series"][i]["data"][j] / 6) / 10

    return jsonify(formatted)


@app.route('/week/pie')
@cross_origin()
def get_pie_week():
    today = datetime.now()
    start_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )-timedelta(days=6, microseconds=1))
    end_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )+timedelta(days=1))
    data = noti.grab_rows(
        "aw",
        noti.MAIN_TABLE_PATH,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )

    labels = ["study", "hobby", "social", "media",
              "leisure", "waste", "uncategorised"]

    formatted = {
        "series": [{
            "data": [
                {
                    "name": "Study",
                    "y": 0
                }, {
                    "name": "Hobby",
                    "y": 0
                }, {
                    "name": "Social",
                    "y": 0
                }, {
                    "name": "Media",
                    "y": 0
                }, {
                    "name": "Leisure",
                    "y": 0
                }, {
                    "name": "Waste",
                    "y": 0
                }, {
                    "name": "Uncategorised",
                    "y": 0
                }
            ]
        }]
    }

    for row in data:
        tag = row[1]
        duration = row[3]

        tag_index = labels.index(tag)

        formatted["series"][0]["data"][tag_index]["y"] += duration

    for i in formatted["series"][0]["data"]:
        if i["y"] < 10:
            i["y"] = None
        else:
            i["y"] = round(i["y"] / 6) / 10

    return jsonify(formatted)


@app.route('/week/timeline')
@cross_origin()
def get_timeline_week():
    today = datetime.now()
    start_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )-timedelta(days=6, microseconds=1))
    end_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )+timedelta(days=1))
    data = noti.grab_rows(
        "aw",
        noti.MAIN_TABLE_PATH,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )

    labels = ["study", "hobby", "social", "media",
              "leisure", "waste", "uncategorised"]
    colors = ["#7fbbb3", "#3f5865", "#a7c080",
              "#e69875", "#dbbc7f", "#7a8478", "#5d6b66"]

    unf = []

    epoch = datetime.utcfromtimestamp(0)

    for event in data:
        timestamp = noti.parse_timestamp(event[2])
        default_day = datetime(year=today.year,
                               month=today.month,
                               day=today.day,
                               hour=timestamp.hour, 
                               minute=timestamp.minute,
                               second=timestamp.second, 
                               microsecond=timestamp.microsecond)
        x = (default_day - epoch).total_seconds() * 1000
        x2 = x + (event[3] * 1000)
        y = (default_day - datetime(year=timestamp.year, month=timestamp.month, day=timestamp.day)).days
        color = colors[labels.index(event[1])]
        unf.append({
            "x": x,
            "x2": x2,
            "y": y,
            "name": event[0],
            "color": color
        })

    return jsonify({"series": unf})

@app.route("/week/timeline/y")
@cross_origin()
def get_timeline_week_x():
    today = datetime.now()
    start_timestamp = datetime(
        today.year,
        today.month,
        today.day
    )-timedelta(days=4, microseconds=1)

    timestamps = [noti.format_timestamp(start_timestamp, simple=True)]

    for i in range(6):
        timestamps.append(noti.format_timestamp(start_timestamp + timedelta(days=i), simple=True))

    timestamps.reverse()

    return(jsonify(timestamps))

@app.route('/week/last_columns')
@cross_origin()
def get_columns_week():

    last_n = int(request.args["n"])


    today = datetime.now()

    week_num = today.weekday()

    start_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )-timedelta(days=((last_n-1)*7)+week_num))
    end_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )+timedelta(days=1))
    data = noti.grab_rows(
        "aw",
        noti.MAIN_TABLE_PATH,
        start_timestamp=start_timestamp,
        end_timestamp=end_timestamp
    )

    labels = ["study", "hobby", "social", "media",
              "leisure", "waste", "uncategorised"]

    formatted = {
        "series": [
            {
                "name": "study",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "hobby",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "social",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "media",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "leisure",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "waste",
                "data": list(np.zeros(last_n)),
                "type": "column"
            },
            {
                "name": "uncategorised",
                "data": list(np.zeros(last_n)),
                "type": "column"
            }]
    }

    for row in data:
        tag_index = labels.index(row[1])
        timestamp = noti.parse_timestamp(row[2])
        day_index = timestamp.isocalendar().week - \
            noti.parse_timestamp(start_timestamp).isocalendar().week
        formatted["series"][tag_index]["data"][day_index] += row[3]

    for i in range(len(formatted["series"])):
        for j in range(last_n):
            formatted["series"][i]["data"][j] = round(
                formatted["series"][i]["data"][j] / 6) / 10

    return jsonify(formatted)


@app.route("/update")
@cross_origin()
def update():
    loader_scribi = importlib.machinery.SourceFileLoader(
        "noti", sys.path[0] + "/../noti-scribi/transc_aw.py")
    spec_scribi = importlib.util.spec_from_loader("noti", loader_scribi)
    noti_scribi = importlib.util.module_from_spec(spec_scribi)
    loader_scribi.exec_module(noti_scribi)

    noti_scribi.main()

    return jsonify({"status": 1})


app.run()
