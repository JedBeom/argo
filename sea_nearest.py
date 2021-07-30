import requests
from bs4 import BeautifulSoup as bs

import pandas as pd

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from haversine import haversine
from init import seas

def get_pts_list(data) -> list:
    r = requests.get(data['ts_url'])
    html = bs(r.content, 'html.parser')
    trs = html.body.find("table").find("table").find_all("tr")[2:]
    pts = (list(), list(), list())
    for tr in trs:
        tds = tr.find_all("td")

        for l in range(len(pts)):
            pts[l].append(float(tds[l].get_text()))

    return pts

def calc_nearest_and_get_pts_list(datas) -> tuple:
    nearest_data_each_seas = pd.DataFrame()
    pts_list = list()

    for sea in seas:
        least_dis = 100000
        nearest_data = None

        for _, data in datas.iterrows():
            dis = haversine((float(data['latitude']), float(data['longtitude'])), sea)
            if (dis < least_dis):
                least_dis = dis
                nearest_data = data

        nearest_data_each_seas = nearest_data_each_seas.append(nearest_data)
        datas = datas.loc[datas['id'] != nearest_data['id']]

        pts = get_pts_list(nearest_data)
        pts_list.append(pts)
    
    return (nearest_data_each_seas, pts_list)

def get_subplot_titles(datas) -> list:
    subplot_titles = list()
    for _, data in datas.iterrows():
        title = f"[{data['id']}] {data['latitude']}N {data['longtitude']}E ({data['date']})"
        subplot_titles.append(title)
    
    return subplot_titles

def show_fig(datas, pts_list) -> None:

    subplot_titles = get_subplot_titles(datas)
    fig = make_subplots(rows=3, cols=1, subplot_titles=subplot_titles)

    for i in range(len(datas)):
        p, t, s = pts_list[i]
        fig.append_trace(go.Scatter(x=s, y=t, mode="markers", marker_color=p, text=p), row=(i+1), col=1)

    fig.update_xaxes(title_text="염분")
    fig.update_yaxes(title_text="수온")
    fig.update_layout(title=f"T-S도")
    fig.show()