import requests
import bs4
from bs4 import BeautifulSoup as bs
import pandas as pd

from init import TsData

host = "http://argo.nims.go.kr/argo3/"

def get_argo_data_list() -> dict:
    path = "argo-all.html?yy=2021&mm=07&land=1"

    html = requests.get(host+path)
    soup = bs(html.content, 'html.parser')

    all_list = soup.body.find("div", "sub-all__list")
    paths = dict()
    for u in all_list.children:
        if type(u) is bs4.element.NavigableString:
            continue

        paths[u.get_text()] = u.attrs["href"]

    return paths

def parse_argo(id, path) -> TsData:
    r = requests.get(host+path)
    soup = bs(r.content, "html.parser") 
    trs = soup.body.find("div", "sub-all__tb").find("tbody").find_all("tr")

    # return only latest data
    tds = trs[0].find_all("td")
    return TsData(id, tds)

def get_latest_argo_data() -> pd.DataFrame:
    paths = get_argo_data_list()
    datas = list()
    for id, path in paths.items():
        data = parse_argo(id, path)
        datas.append(data)

    df = pd.DataFrame([(d.id, d.date, d.pn, d.latitude, d.longtitude, d.ts_url) for d in datas], columns=['id', 'date', 'pn', 'latitude', 'longtitude', 'ts_url'])
    return df