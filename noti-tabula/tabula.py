from nicegui import ui
import requests


ui.dark_mode().enable()
ui.query('body').style(f'background-color: #333c43; color: #d3c6aa')

ui.colors(
    primary="#3f5865",
    secondary="#a7c080",
    accent="#d699b6",
    dark="#3a464c"
)

def update():
    ui.notify("Updating...")
    requests.get("http://127.0.0.1:5000/update")
    week_column_chart.options["series"] = requests.get("http://127.0.0.1:5000/week/column").json()["series"]
    week_column_chart.update()
    ui.notify("Success!")

    

with ui.row() as header_row:
    ui.label("Data for 2023-06-05:").classes("text-4xl")
    header_row.classes("place-self-center w-4/5")

with ui.row() as opts_row:
    ui.button("<", color="#3f5865").props("unelevated").classes("h-8")
    ui.toggle(["Day", "Week", "Month"], value="Day").props("unelevated color=dark text-color=d3c6aa").classes("max-h-8")
    ui.button(">", color="#3f5865").props("unelevated").classes("h-8")

    ui.button("Update", on_click=update, color="#3f5865").props("unelevated").classes("h-8")

    opts_row.classes("place-self-center w-4/5")
    
week_column_chart = ui.chart({
    "title": False,
    "chart": {
        "type": "column",
        "backgroundColor": "#3a464c",
        "spacingTop": 24
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
        "categories": [
            "2023-05-30",
            "2023-05-31",
            "2023-06-01",
            "2023-06-02",
            "2023-06-03",
            "2023-06-04",
            "2023-06-05"
        ],
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
    "series": requests.get("http://127.0.0.1:5000/week/column").json()["series"],
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
}).classes("w-4/5 h-48 rounded-md place-self-center")

today_pie_chart = ui.chart({
    "title": False,
    "chart": {
        "type": "pie",
        "backgroundColor": "#3a464c"
    },
    "series": requests.get("http://127.0.0.1:5000/today/pie").json()["series"],
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
            "borderColor": None
        }
    }
}).classes("w-1/5 h-96 rounded-md place-self-center")

ui.run()