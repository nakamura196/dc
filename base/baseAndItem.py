import os
import requests
import time
from bs4 import BeautifulSoup
import glob
from tqdm import tqdm
import json
import copy

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
result2 = []

for page in map:

    if page < 1:
        continue

    label = []

    for line in map[page]:
        label.append(map[page][line])

    obj = {
        "page" : page,
        "type": "ページ",
        "vol_str" : "01 伊勢物語",
        "vol" : 1,
        "objectID" : str(page).zfill(5),
        "target" : collection,
        "related" : {},
        "attribution" : attribution
     }

    fw2 = open("docs/item/{}/{}.json".format(collection, str(page).zfill(5)), 'w')
    json.dump(obj, fw2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

    obj2 = copy.deepcopy(obj)

    obj2["label"] = label
    obj2["text"] = "\n".join(label)

    result.append(obj)
    result2.append(obj2)

fw2 = open("data/base/{}.json".format(collection), 'w')
json.dump(result2, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

fw2 = open("docs/base/{}.json".format(collection), 'w')
json.dump(result, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))