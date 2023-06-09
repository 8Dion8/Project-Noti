import json, sys, os
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

@app.route('/today/timeline')
@cross_origin()
def get_timeline_today(_format=True):
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
    if _format:
        return jsonify(noti.format_for_apexcharts(AW_DATA))
    else:
        return AW_DATA

@app.route('/today/pie')
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

    labels = ["study", "hobby", "social", "media", "leisure", "waste", "uncategorised"]

    formatted = {
        "series": [{
            "data": [
                {
                    "name": "Study",
                    "y": 0
                },{
                    "name": "Hobby",
                    "y": 0
                },{
                    "name": "Social",
                    "y": 0
                },{
                    "name": "Media",
                    "y": 0
                },{
                    "name": "Leisure",
                    "y": 0
                },{
                    "name": "Waste",
                    "y": 0
                },{
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
            i["y"] = round(i["y"] / 6) /10

    

    return jsonify(formatted)

@app.route('/today/heat')
@cross_origin()
def get_heat_today():
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

    labels = ["study", "hobby", "social", "media", "leisure", "waste", "uncategorised"]

    unf = list(np.zeros((len(labels), 24*6)))

    formatted = []

    for row in data:
        tag = row[1]
        duration = row[3]
        tag_index = labels.index(tag)
        timestamp = noti.parse_timestamp(row[2])
        time_index = timestamp.hour * 6 + timestamp.minute // 10

        while True:
            s = unf[tag_index][time_index]
            if duration + s > 600:
                unf[tag_index][time_index] = 600
                duration -= 600 - s
                time_index += 1
            else:
                unf[tag_index][time_index] += duration
                break

    for i in range(len(labels)):
        for j in range(24*6):
            formatted.append([j, i, unf[i][j] / 600])

    return jsonify({"series": formatted})
        


@app.route('/last/column')
@cross_origin()
def get_grid_column():

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
   

    labels = ["study", "hobby", "social", "media", "leisure", "waste", "uncategorised"]

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
            formatted["series"][i]["data"][j] = round(formatted["series"][i]["data"][j] / 6) /10

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
