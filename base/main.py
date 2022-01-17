import os
import requests
import time
from bs4 import BeautifulSoup
import glob
from tqdm import tqdm
import json

collection = "eiga"

files = glob.glob("data/{}/*.html".format(collection))

result = {}

files = sorted(files)

for i in tqdm(range(len(files))):

    path = files[i]

    # シフトJISエンコードのテキストファイルの読み込み
    with open(path, encoding='utf-8', errors='ignore') as f:
        s = f.read()

    soup = BeautifulSoup(open(path), 'html.parser')

    sp = str(soup).split("<hr/>")[2].split("<br/>")

    if len(sp) > 1:

        line = sp[0].strip()

        prefix = line.split(" ")[0].strip().replace("�", "")

        text = line[len(prefix)+1:][1:].strip()

        if prefix not in result:
            result[prefix] = text

        if prefix == "0528-09":
            print(path)

    else:
        os.remove(path)

    if i > 30000:
        # pass
        break

# print(result)

fw2 = open("data/" + collection +".json", 'w')
json.dump(result, fw2, ensure_ascii=False, indent=4,
            sort_keys=True, separators=(',', ': '))