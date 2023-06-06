import json, sys, os
from flask import Flask, jsonify
from flask_cors import CORS, cross_origin
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

    return jsonify(formatted)

@app.route('/week/column')
@cross_origin()
def get_grid_column():
    today = datetime.now()
    start_timestamp = noti.format_timestamp(datetime(
        today.year,
        today.month,
        today.day
    )-timedelta(days=6))
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
                "data": [0,0,0,0,0,0,0]
            },
            {
                "name": "hobby",
                "data": [0,0,0,0,0,0,0]
            },
            {
                "name": "social",
                "data": [0,0,0,0,0,0,0]
            },
            {
                "name": "media",
                "data": [0,0,0,0,0,0,0]
            },
            {
                "name": "leisure",
                "data": [0,0,0,0,0,0,0]
            },
            {
                "name": "waste",
                "data": [0,0,0,0,0,0,0]
            },
            {
                "name": "uncategorised",
                "data": [0,0,0,0,0,0,0]
            }]
    }

    for row in data:
        tag_index = labels.index(row[1])
        timestamp = noti.parse_timestamp(row[2])
        day_index = (timestamp - noti.parse_timestamp(start_timestamp)).days
        formatted["series"][tag_index]["data"][day_index] += row[3]
    
    for i in range(len(formatted["series"])):
        for j in range(7):
            formatted["series"][i]["data"][j] = round(formatted["series"][i]["data"][j] / 60)

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
