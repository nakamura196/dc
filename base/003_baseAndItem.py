import os
import requests
import time
from bs4 import BeautifulSoup
import glob
from tqdm import tqdm
import json
import copy
import json
import argparse    # 1. argparseをインポート


parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id')
parser.add_argument('--padding', "-p", type=int, default=1)

args = parser.parse_args()    # 4. 引数を解析

collection = args.id
attribution = "新編 日本古典文学全集"

path = "data/{}_merged.json".format(collection)

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

    path = "../docs/item/{}/{}.json".format(collection, str(page).zfill(5))
    os.makedirs(os.path.dirname(path), exist_ok=True)

    fw2 = open(path, 'w')
    json.dump(obj, fw2, ensure_ascii=False, indent=4,
                sort_keys=True, separators=(',', ': '))

    obj2 = copy.deepcopy(obj)

    obj2["label"] = label
    obj2["text"] = "\n".join(label)

    result.append(obj)
    result2.append(obj2)

fw2 = open("data/{}.json".format(collection), 'w')
json.dump(result2, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))

fw2 = open("../docs/base/{}.json".format(collection), 'w')
json.dump(result, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))