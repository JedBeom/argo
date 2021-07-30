import datetime

class TsData():
    id = ""
    date = ""
    pn = ""
    latitude = ""
    longtitude = ""
    ts_url = ""

    def __init__(self, id, tds) -> None:
        self.id = id
        self.date = datetime.datetime.strptime(tds[0].get_text(), "%Y년 %m월 %d일 %H시 %M분 %S초")
        self.pn = tds[1].get_text()
        self.latitude = tds[2].get_text()
        self.longtitude = tds[3].get_text()

        self.latitude = float(self.latitude[:len(self.latitude)-1])
        self.longtitude = float(self.longtitude[:len(self.longtitude)-1])

        dir_list_unpurified = tds[6].find_all("a")[1].attrs["href"].split(",")[3][1:]
        dir_list = dir_list_unpurified[:len(dir_list_unpurified)-3]

        self.ts_url = f"http://argo.nims.go.kr/data/float_text_view1.php?sel=1&wmo_id={id}&cycle_number={self.pn.zfill(3)}&dir_list={dir_list}&mode=R"
    
    def __str__(self) -> str:
        return f"[{self.id}] {self.date} {self.ts_url}"

east_sea = (38.239723, 130.864291)
# south_sea = (33.884506, 127.209461)
west_sea = (37.007446, 124.301821)

seas = [east_sea, west_sea]