from get_from_argo import get_latest_argo_data
from sea_nearest import calc_nearest_and_get_pts_list, show_fig
import datetime

s = datetime.datetime.now()

datas = get_latest_argo_data()
nearest, pts_each = calc_nearest_and_get_pts_list(datas)

show_fig(nearest, pts_each)

print(datetime.datetime.now() - s)