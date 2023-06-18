from nicegui import ui, app
import requests
import sys
from datetime import datetime
from datetime import timedelta

import importlib.machinery
import importlib.util
loader = importlib.machinery.SourceFileLoader(
    "noti", sys.path[0] + "/../noti-bibli/noti.py")
spec = importlib.util.spec_from_loader("noti", loader)
noti = importlib.util.module_from_spec(spec)
loader.exec_module(noti)


today = datetime.now()

n=10

last_n_timestamps = [noti.format_timestamp(datetime(today.year, today.month, today.day)-timedelta(days=n-1-i), simple=True) for i in range(n)]


ui.dark_mode().enable()
ui.query('body').style(f'background-color: #333c43; color: #d3c6aa')

ui.colors(
    primary="#3f5865",
    secondary="#a7c080",
    accent="#d699b6",
    dark="#3a464c"
)

def update():
    cur_period = period_toggle.value.lower()
    ui.notify(f"Updating for current {cur_period}...")
    requests.get("http://127.0.0.1:5000/update")

    chart00.options["series"] = requests.get(f"http://127.0.0.1:5000/{cur_period}/last_columns?n={n}").json()["series"]
    chart00.update()
    chart10.options["series"] = requests.get(f"http://127.0.0.1:5000/{cur_period}/pie").json()["series"]
    chart10.update()
    chart11.options["series"][0]["data"] = requests.get(f"http://127.0.0.1:5000/{cur_period}/timeline").json()["series"]
    chart11.options["yAxis"]["categories"] = requests.get(f"http://127.0.0.1:5000/{cur_period}/timeline/y").json()
    chart11.update()
    

    ui.notify("Success!")


def calc_time_passed():

    dif = datetime.now() - noti.parse_timestamp(noti.get_config("aw", "last_updated"))
    secs = int(dif.total_seconds())

    if secs == 1:
        return "1 second"
    elif secs < 60:
        return f"{secs} seconds"
    elif secs < 120:
        return "1 minute"
    elif secs < 3600:
        return f"{secs//60} minutes"
    elif secs < 7200:
        return "1 hour"
    elif secs < 86400:
        return f"{secs//3600} hours"
    elif secs < 172800:
        return "1 day"
    else:
        return f"{secs // 86400} days"
    

with ui.row() as header_row:
    ui.label(f"Data for {last_n_timestamps[-1]}:").classes("text-4xl")
    header_row.classes("place-self-center w-[80vw]")

with ui.row() as opts_row:
    ui.button("<", color="#3f5865").props("unelevated").classes("h-8")
    period_toggle = ui.toggle(["Day", "Week", "Month"], value="Day", on_change=update).props("unelevated color=dark text-color=d3c6aa").classes("max-h-8")
    ui.button(">", color="#3f5865").props("unelevated").classes("h-8")

    ui.button("Update", on_click=update, color="#3f5865").props("unelevated").classes("h-8")
    ago_label = ui.label().classes("h-8 text-l place-self-center")
    ui.timer(5.0, lambda: ago_label.set_text(calc_time_passed()))

    opts_row.classes("place-self-center w-[80vw]")
    
chart00 = ui.chart({
    "title": False,
    "chart": {
        "type": "column",
        "backgroundColor": "#3a464c",
        "spacingTop": 24,
        "spacingBottom": 24
    },
    "yAxis": {
        "tickInterval": 60,
        "minorTicks": True,
        "minorTickInterval": 15,
        "minorGridLineColor": "#434f55",
        "gridLineColor": "#4d5960",
        "lineColor": "#4d5960",
        "title": {
            "text": "Minutes",
            "style": {
                "color": "#d3c6aa"
            }
        },
        "labels": {
            "style": {
                "color": "#d3c6aa"
            }
        }
    },
    "xAxis": {
        "categories": last_n_timestamps,
        "lineColor": "#4d5960",
        "labels": {
            "style": {
                "color": "#d3c6aa"
            }
        },
        "crosshair": True
    },
    "legend": {
        "enabled": False
    },
    "series": requests.get(f"http://127.0.0.1:5000/day/last_columns?n={n}").json()["series"],
    "colors": [
        "#7fbbb3",
        "#3f5865",
        "#a7c080",
        "#e69875",
        "#dbbc7f",
        "#7a8478",
        "#5d6b66"
    ],
    "plotOptions": {
        "column": {
            "borderColor": None,
            "borderRadius": 1
        }
    }
}).classes("w-[80vw] h-48 rounded-md place-self-center")

with ui.row() as chart_row0:
    chart10 = ui.chart({
        "title": False,
        "chart": {
            "type": "pie",
            "backgroundColor": "#3a464c",
            "spacingTop": 24,
            "spacingBottom": 24
        },
        "series": requests.get("http://127.0.0.1:5000/day/pie").json()["series"],
        "colors": [
            "#7fbbb3",
            "#3f5865",
            "#a7c080",
            "#e69875",
            "#dbbc7f",
            "#7a8478",
            "#5d6b66"
        ],
        "plotOptions": {
            "pie": {
                "borderColor": None,
                "size": "100%",
                "innerSize": "70%",
                "dataLabels": {
                    "enabled": True,
                    "distance": "-45%",
                    "style": {
                        "color": "#d3c6aa",
                        "textOutline": None,
                        "fontWeight": "500"
                    }
                }
            }
        }
    }).classes("w-[24vw] h-128 rounded-md")

    chart11 = ui.chart({
        "title": False,
        "chart": {
            "type": "xrange",
            "backgroundColor": "#3a464c",
            "spacingTop": 24,
            "spacingBottom": 24
        },
        "xAxis": {
            "type": "datetime",
            "minorGridLineColor": "#434f55",
            "gridLineColor": "#4d5960",
            "lineColor": "#4d5960",
            "labels": {
                "style": {
                    "color": "#d3c6aa"
                }
            },
        },
        "yAxis": {
            "categories": ["Study", "Hobby", "Social", "Media", "Leisure", "Waste", "Uncategorised"],
            "title": None,
            "minorGridLineColor": "#434f55",
            "gridLineColor": "#4d5960",
            "lineColor": "#4d5960",
            "labels": {
                "style": {
                    "color": "#d3c6aa"
                }
            }
        },
        "legend": {
            "enabled": False
        },
        
        "series": [{
            "data": requests.get("http://127.0.0.1:5000/day/timeline").json()["series"],
            "borderRadius": 0,
            "borderWidth": 0
            }]
    },
    extras=["xrange"]).classes("w-[55vw] h-128 rounded-md")

    chart_row0.classes("place-self-center items-stretch")

app.on_connect(update)

ui.run()

