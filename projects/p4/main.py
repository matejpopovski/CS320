# project: p4
# submitter: popovski
# partner: none
# hours: 15

import re
import time
from io import BytesIO
from zipfile import ZIP_DEFLATED, ZipFile

import geopandas
import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
from flask import Flask, Response, jsonify, request
from shapely.geometry import box

import edgar_utils

matplotlib.use("Agg")

app = Flask(__name__)

with ZipFile("server_log.zip") as zf:
    with zf.open("rows.csv") as f:
        df = pd.read_csv(f)
ab = [0, 0]
home_visited = 0
visitors = []
times = {}


@app.route("/")
def home():
    global home_visited
    with open("index.html") as f:
        html = f.read()
    home_visited += 1

    html_blue = html.replace("donate.html", "donate.html?from=A")
    html_red = html.replace("donate.html", "donate.html?from=B")
    html_red = html_red.replace("color:blue;", "color:red;")

    if home_visited <= 10:
        if home_visited % 2 == 1:
            return html_blue
        else:
            return html_red
    else:
        if ab[0] >= ab[1]:
            return html_blue
        else:
            return html_red


@app.route("/browse.html")
def browse_table():
    df_browse_500 = df.head(500)
    table = "<h1>Browse first 500 rows of rows.csv</h1>" + df_browse_500.to_html()
    return table


@app.route("/browse.json")
def browse_json():
    global visitors, times
    df_browse_500 = df.head(500)
    json_source = jsonify(df_browse_500.to_dict("records"))
    rate = 60
    client_ip = request.remote_addr
    visitors.append(client_ip)
    now = time.time()
    if client_ip in times:
        td = now - times[client_ip]
        if td < rate:
            return Response(
                "Too many Requests, Please come back in "
                + str(int(rate - td))
                + " seconds.",
                status=429,
                headers={"Retry-After": str(rate)},
            )
        else:
            times[client_ip] = now
            return json_source
    else:
        times[client_ip] = now
        return json_source


@app.route("/visitors.json")
def visitor_json():
    return visitors


@app.route("/donate.html")
def donation():
    try:
        if request.args["from"] == "A":
            ab[0] = ab[0] + 1
        else:
            ab[1] = ab[1] + 1
    except:
        pass
    text = "<html>{}<html>".format(
        "Thanks in advance for donating some money to support our cause!"
    )
    return "<h1>Donation</h1>" + text


@app.route("/analysis.html")
def analysis():
    dict_ip = {}
    q1 = df.groupby("ip").size().nlargest(10)
    q1 = q1.to_dict()

    sics = []
    addrs_list = {}
    with ZipFile("docs.zip") as zf:
        for name in zf.namelist():
            if name[-1] != "/":
                with zf.open(name) as f:
                    file = f.read().decode("utf-8")
                    sic = edgar_utils.Filing(file).sic
                    if sic != None:
                        sics.append(sic)

                    addrs_in_file = edgar_utils.Filing(file).addresses
                    addrs_list[name] = addrs_in_file

    addrs = []
    for idx, row in df.iterrows():
        path = "/".join([str(int(row["cik"])), row["accession"], row["extention"]])
        if path in addrs_list:
            for addr in addrs_list[path]:
                if addr != "":
                    addrs.append(addr)

    q2 = pd.Series(sics).value_counts().head(10).to_dict()
    counts = pd.Series(addrs).value_counts()
    counts = counts[counts >= 300].to_dict()

    return f"""
    <h1>Analysis of EDGAR Web Logs</h1>
    <p>Q1: how many filings have been accessed by the top ten IPs?</p>
    <p>{str(q1).strip()}</p>
    <p>Q2: what is the distribution of SIC codes for the filings in docs.zip?</p>
    <p>{str(q2).strip()}</p>
    <p>Q3: what are the most commonly seen street addresses?</p>
    <p>{str(counts).strip()}</p>
    <h4>Dashboard: geographic plotting of postal code</h4>
    <img src="dashboard.svg">
    """


@app.route("/dashboard.svg")
def dashboard():
    west, east, north, south = -95, -60, 50, 25
    us_states_gcs = geopandas.read_file("shapes/cb_2018_us_state_20m.shp").intersection(
        box(west, south, east, north)
    )
    locations_gcs = geopandas.read_file("locations.geojson")
    locations_gcs = locations_gcs[
        locations_gcs["geometry"].intersects(box(west, south, east, north))
    ]
    locations_gcs["zip_code"] = 0

    for idx, row in locations_gcs.iterrows():
        results = re.findall(r"[A-Z]{2}\s([0-9]{5})$", row["address"])
        if len(results) >= 1:
            locations_gcs.at[idx, "zip_code"] = int(results[0])
        results = re.findall(r"[A-Z]{2}\s([0-9]{5})-[0-9]{4}$", row["address"])
        if len(results) >= 1:
            locations_gcs.at[idx, "zip_code"] = int(results[0])

    locations_gcs = locations_gcs[locations_gcs["zip_code"] >= 25000]
    locations_gcs = locations_gcs[locations_gcs["zip_code"] <= 65000]
    us_states = us_states_gcs.to_crs("epsg:2022")
    locations = locations_gcs.to_crs("epsg:2022")

    fig, ax = plt.subplots()
    fig, ax = plt.subplots()
    us_states.plot(color="lightgray", ax=ax)
    locations.plot(
        locations_gcs.zip_code, cmap="RdBu", ax=ax, legend=True, markersize=50
    ).axis("off")

    fake_file = BytesIO()
    fig.savefig("dashboard.svg")
    fig.savefig(fake_file, format="svg")
    plt.close(fig)

    return Response(fake_file.getvalue(), headers={"Content-Type": "image/svg+xml"})


if __name__ == "__main__":
    # REMOVE PORT 8000 before submiting
    app.run(
        host="0.0.0.0", port="8000", debug=True, threaded=False
    )  # don't change this line!
