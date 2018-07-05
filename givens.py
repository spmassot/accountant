from ipywidgets import Text, DatePicker, HBox, VBox
from IPython.display import display
from itertools import chain
import pandas as pd
import xlrd
import os
import re

start_date = DatePicker()
end_date = DatePicker()
month = Text(placeholder='month')
widgies = VBox([HBox([start_date,end_date]),month])
display(widgies)

path_name = '/mnt/c/Users/Sean/Desktop/AudioVox/Givens/'
files = [x for x in os.listdir(path_name)]
all_dfs = []
all_adj_dfs = []
for fil_ in files:
    print(fil_)
    xls = xlrd.open_workbook(path_name+fil_, on_demand=True)
    main_sought = ['Brampton','Chesapeake','Plainfield','Reno','Hope']
    adj_sought = [x+' Adjustments' for x in main_sought]
    matched = [x for x in xls.sheet_names() if x in main_sought]
    print(matched)
    adj_matched = [x for x in xls.sheet_names() if x in adj_sought]
    print(adj_matched)
    list_frames = [pd.read_excel(
            path_name+fil_,
            sheetname=mtch,
            header=7,
            converters={"ORDER #'s":str}
        ).dropna(thresh=12) for mtch in matched]
    list_adj_frames = [pd.read_excel(
            path_name+fil_,
            sheetname=mtch,
            header=7,
            converters={"ORDER #'s":str}
        ).dropna(thresh=4) for mtch in adj_matched]

    new_df = pd.concat(list_frames, ignore_index=True)
    new_adj_df = pd.concat(list_adj_frames, ignore_index=True)

    all_dfs.append(new_df)
    all_adj_dfs.append(new_adj_df)

big_df = pd.concat(all_dfs, ignore_index=True)
big_adj_df = pd.concat(all_adj_dfs, ignore_index=True)
big_df = big_df[
    (str(start_date.value) <= big_df['SHIP DATE']
    ) & (str(end_date.value) >= big_df['SHIP DATE'])
]
big_df.to_csv(f'/mnt/c/Users/Sean/Desktop/AudioVox/givens_{month.value}.csv')
big_adj_df.to_csv(f'/mnt/c/Users/Sean/Desktop/AudioVox/givens_adj_{month.value}.csv')

print('Done!')

pick_tick = re.compile('\d{7}')
pts = zip(
    list(big_df['TOTAL']),
    [pick_tick.findall(str(x)) for x in list(big_df["ORDER #'s"])]
)
adj_pts = zip(
    list(big_adj_df['TOTAL']),
    [pick_tick.findall(str(x)) for x in list(big_adj_df["ORDER #'s"])]
)

def flatten(in_list):
    out_list = []
    for x in in_list:
        l = [x[0]]
        l.extend(list(chain(x[1])))
        out_list.append(l)
    return out_list

zz = flatten(pts)
zz_adj = flatten(adj_pts)
pd.DataFrame(zz).to_csv(f'/mnt/c/Users/Sean/Desktop/AudioVox/givens_{month.value}_flat.csv')
pd.DataFrame(zz_adj).to_csv(f'/mnt/c/Users/Sean/Desktop/AudioVox/givens_adj_{month.value}_flat.csv')

yyyy = []
for x in zip(
    list(big_df['TOTAL']),
    [pick_tick.findall(str(x)) for x in list(big_df["ORDER #'s"])]
):
    yyyy.extend(list(chain(x[1])))

zzzz = []
for x in zip(
    list(big_adj_df['TOTAL']),
    [pick_tick.findall(str(x)) for x in list(big_adj_df["ORDER #'s"])]
):
    zzzz.extend(list(chain(x[1])))

yyyy.extend(zzzz)
aaaa_a = set(yyyy)
_a_ = pd.Series(list(aaaa_a))
_a_.to_csv(f'/mnt/c/Users/Sean/Desktop/AudioVox/givens_{month.value}_pts.csv')

## Run the access query, then ...

lookr = pd.read_csv(
    f'/mnt/c/Users/Sean/Desktop/AudioVox/{month.value}_aq.csv'
).dropna(0, thresh=3).sort_values('SumOfCOST',ascending=False)
givs = pd.DataFrame(zz)
adj_givs = pd.DataFrame(zz_adj)

def get_maps(in_df):
    return (
        in_df.applymap(lambda x:get_one('SumOfCOST',x)),
        in_df.applymap(lambda x:get_one('COMPANY',x)),
        in_df.applymap(lambda x:get_one('PRD5',x))
    )

def get_one(header, value):
    if not value:
        return None
    try:
        return list(lookr.loc[lookr['thing']==int(value)][header])[0]
    except Exception as e:
        return None

maps = get_maps(givs[givs.columns[1:]])
adj_maps = get_maps(adj_givs[adj_givs.columns[1:]])

def get_match(val):
    try:
        return val[high_cost[val.name]]
    except:
        return '#N/A'

def adj_get_match(val):
    try:
        return val[adj_high_cost[val.name]]
    except:
        return '#N/A'

high_cost = maps[0].apply(pd.Series.argmax, axis=1)
company = maps[1].apply(lambda x:get_match(x), axis=1)
lob = maps[2].apply(lambda x:get_match(x), axis=1)

adj_high_cost = adj_maps[0].apply(pd.Series.argmax, axis=1)
adj_company = adj_maps[1].apply(lambda x:adj_get_match(x), axis=1)
adj_lob = adj_maps[2].apply(lambda x:adj_get_match(x), axis=1)

pd.DataFrame([company,lob]).T.to_csv(
    f'/mnt/c/Users/Sean/Desktop/AudioVox/givens_{month.value}_lookups.csv')
pd.DataFrame([adj_company,adj_lob]).T.to_csv(
    f'/mnt/c/Users/Sean/Desktop/AudioVox/givens_{month.value}_adj_lookups.csv')

