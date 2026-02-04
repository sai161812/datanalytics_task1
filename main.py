import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, time
import pytz

data = pd.read_csv("playstoredata.csv")

def clean_installs(value):
    if isinstance(value, str):
        value = value.replace("+", "").replace(",", "")
    return pd.to_numeric(value, errors="coerce")

data["Installs"] = data["Installs"].apply(clean_installs)

def parse_size(size):
    if isinstance(size, str):
        size = size.strip()
        if size.endswith("M"):
            return float(size[:-1])
        if size.endswith("k"):
            return float(size[:-1]) / 1024
    return None

data["Size_MB"] = data["Size"].apply(parse_size)

data = data.dropna(subset=["Rating"])
data["Last Updated"] = pd.to_datetime(data["Last Updated"], errors="coerce")

qualified_apps = data[
    (data["Rating"] >= 4.0) &
    (data["Size_MB"] >= 10) &
    (data["Last Updated"].dt.month == 1)
]

top_categories = (
    qualified_apps
    .groupby("Category")["Installs"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .index
)

top_apps = qualified_apps[qualified_apps["Category"].isin(top_categories)]

summary = (
    top_apps
    .groupby("Category")
    .agg(
        Average_Rating=("Rating", "mean"),
        Review_Count=("Reviews", "sum")
    )
    .reset_index()
)

chart = go.Figure()

chart.add_bar(
    x=summary["Category"],
    y=summary["Average_Rating"],
    name="Average Rating"
)

chart.add_bar(
    x=summary["Category"],
    y=summary["Review_Count"],
    name="Total Reviews"
)

chart.update_layout(
    title="Top 10 App Categories: Rating vs Review Volume",
    xaxis_title="Category",
    yaxis_title="Value",
    barmode="group",
    xaxis_tickangle=-45
)

ist_zone = pytz.timezone("Asia/Kolkata")
current_ist_time = datetime.now(ist_zone).time()

allowed_start = time(15, 0) 
allowed_end = time(17, 0)  

if allowed_start <= current_ist_time <= allowed_end:
    chart.write_html("app_category_analysis.html")
    print("Chart generated successfully: app_category_analysis.html")
else:
    print("Chart access is restricted to 3:00 PM – 5:00 PM IST.")
