import os
import requests
import time
from bs4 import BeautifulSoup
import glob
from tqdm import tqdm
import json

collection = "ise"
attribution = "新編 日本古典文学全集"

path = "data/{}.json".format(collection)

with open(path) as f:
    df = json.load(f)

map = {}

for key in df:
    id = key
    spl = id.split("-")
    page = int(spl[0])
    line = int(spl[1])

    if page not in map:
        map[page] = {}

    map[page][line] = df[key]

result = []

for page in map:

    if page < 1:
        continue

    label = []

    for line in map[page]:
        label.append(map[page][line])

    obj = {
        "label" : label,
        "page" : page,
        "type": "ページ",
        "vol_str" : "01 伊勢物語",
        "vol" : 1,
        "objectID" : str(page).zfill(5),
        "text" : "\n".join(label),
        "target" : collection,
        "related" : {},
        "attribution" : attribution
     }

    fw2 = open("data/item/{}/{}.json".format(collection, str(page).zfill(5)), 'w')
    json.dump(obj, fw2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

    result.append(obj)

fw2 = open("data/base/{}.json".format(collection), 'w')
json.dump(result, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))