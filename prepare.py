import json
import requests
import os
import shutil
import gzip

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id')
parser.add_argument('collection')

args = parser.parse_args()    # 4. 引数を解析

id = args.id
collection = args.collection

'''

import argparse    # 1. argparseをインポート

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id')
# parser.add_argument('password')
# parser.add_argument('--reverse', "-r", default=False, type=bool)
# parser.add_argument('--collection', "-c", default="https://script.google.com/macros/s/AKfycbweFcBogWLgf7AyFboBOAnKxqeJr_cVQEk3PPODAEA5KBgr_rywx6IQm8ug5MS-A5F1/exec?sheet=all")

args = parser.parse_args()    # 4. 引数を解析

id = args.id
password = args.password
reverse = args.reverse

args = parser.parse_args()    # 4. 引数を解析

'''

# id = "ise"

url = "https://script.google.com/macros/s/AKfycbybV8sJwAGwnJ5B4ll7C9bIWWWTg_nepAxmTVpz2vgfNUeehIJ1b1WIfj07FDCANgu-Cg/exec?sheet=main"

df = requests.get(url).json()

lines = []
lines.append("set -e")
lines.append("cd ../")

def isExists():
  return True

for item in df:
  if item["id"] == id:
    gas_url = item["gas"]
    gas = requests.get(gas_url).json()
    
    # print("gas", gas_url)

    sheets = gas[1:]

    for sheet in sheets:
      for value in sheet["value"]:
        file_id = value["id"]

        print("fid", file_id)

        tmp_path = "data/text/" + file_id + "/text.json.gzip"

        if not os.path.exists(tmp_path):

          os.makedirs(os.path.dirname(tmp_path), exist_ok=True)

          gzip_url = "https://github.com/nakamura196/kocr/blob/main/docs/runs/model_codh/output/{}/text.json.gzip?raw=true".format(file_id)

          try:
            print("url", gzip_url)
            urlData = requests.get(gzip_url).content          

            with open(tmp_path ,mode='wb') as f: # wb でバイト型を書き込める
              f.write(urlData)

            with gzip.open(tmp_path, 'r') as f:
              df = json.load(f)

          except Exception as e:
            print(e)
            continue

        lines.append("python 000_text.py '{}'".format(file_id))
        lines.append("python 002_calc.py '{}' '{}'".format(file_id, collection))
        lines.append("python 004_updateItem.py '{}' '{}'".format(file_id, collection))

with open("sh/{}.sh".format(collection), mode='w') as f:
  f.write("\n".join(lines))