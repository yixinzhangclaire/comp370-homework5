import csv
from collections import defaultdict
from datetime import datetime

from bokeh.io import curdoc
from bokeh.layouts import column
from bokeh.models import Select, ColumnDataSource
from bokeh.plotting import figure


data = defaultdict(dict)
zipcodes = set()

with open("monthly_response_times.csv", newline="", encoding="utf-8") as f:
    reader = csv.DictReader(f)

    for row in reader:
        zipcode = row["zipcode"]
        month = row["month"]
        avg = float(row["average_response_hours"])

        data[zipcode][month] = avg

        if zipcode != "ALL":
            zipcodes.add(zipcode)


zipcodes = sorted(zipcodes)

zip1 = Select(
    title="Zipcode 1",
    value=zipcodes[0],
    options=zipcodes
)

zip2 = Select(
    title="Zipcode 2",
    value=zipcodes[1],
    options=zipcodes
)


def make_series(zipcode):
    months = sorted(
        month for month in data[zipcode].keys()
        if month.startswith("2024-")
    )

    x = [
        datetime.strptime(month, "%Y-%m")
        for month in months
    ]

    y = [
        data[zipcode][month]
        for month in months
    ]

    return x, y


all_x, all_y = make_series("ALL")
zip1_x, zip1_y = make_series(zip1.value)
zip2_x, zip2_y = make_series(zip2.value)


source_all = ColumnDataSource(
    data=dict(x=all_x, y=all_y)
)

source_zip1 = ColumnDataSource(
    data=dict(x=zip1_x, y=zip1_y)
)

source_zip2 = ColumnDataSource(
    data=dict(x=zip2_x, y=zip2_y)
)


plot = figure(
    title="Monthly Average 311 Response Time",
    x_axis_type="datetime",
    width=900,
    height=500
)

plot.line(
    "x",
    "y",
    source=source_all,
    line_width=2,
    legend_label="ALL"
)

plot.line(
    "x",
    "y",
    source=source_zip1,
    line_width=2,
    legend_label="Zipcode 1"
)

plot.line(
    "x",
    "y",
    source=source_zip2,
    line_width=2,
    legend_label="Zipcode 2"
)

plot.xaxis.axis_label = "Month"
plot.yaxis.axis_label = "Average response time (hours)"
plot.legend.location = "top_left"


def update(attr, old, new):
    x1, y1 = make_series(zip1.value)
    x2, y2 = make_series(zip2.value)

    source_zip1.data = dict(x=x1, y=y1)
    source_zip2.data = dict(x=x2, y=y2)


zip1.on_change("value", update)
zip2.on_change("value", update)


curdoc().add_root(
    column(
        zip1,
        zip2,
        plot
    )
)

curdoc().title = "NYC 311 Response Time Dashboard"
