import argparse    # 1. argparseをインポート
import json
import requests
import hashlib
import json
import gzip
import os

parser = argparse.ArgumentParser(description='このプログラムの説明（なくてもよい）')    # 2. パーサを作る

# 3. parser.add_argumentで受け取る引数を追加していく
parser.add_argument('id')
# parser.add_argument('attribution')
# parser.add_argument('name')

args = parser.parse_args()    # 4. 引数を解析

file_id = args.id

attribution = file_id.split("_")[0] # "attribution" # args.attribution

name = file_id # "name"  # args.name

vol = int(file_id.split("-")[-1])

root = "/Users/nakamurasatoru/git/d_hi_letter/yolov5-flask-kunshujo/docs/runs/model_codh"
# file_id = "ndl_1288457-01"

vol = int(file_id.split("-")[-1])

target = file_id.replace("-" + file_id.split("-")[-1], "")

conf_vol = vol

######

def getManifestData(manifest):
  pages = {}
  m_data = requests.get(manifest).json()

  canvases = m_data["sequences"][0]["canvases"]

  images = {}

  for i in range(len(canvases)):
      page = i+1
      canvas = canvases[i]
      canvas_id = canvas["@id"]

      if "thumbnail" in canvas:
          images[canvas_id] = canvas["thumbnail"]["@id"]
      else:
          images[canvas_id] = canvas["images"][0]["resource"]["service"]["@id"] + "/full/200,/0/default.jpg"

      pages[canvas_id] = page

  return pages, images

def getCanvasTextMap(members):
  # canvas毎のテキストを取得
  member_map = {}
  canvas_map = {}
  for member in members:
    member_id = member["@id"]

    anno_id = member["metadata"][0]["value"][0]["@id"]

    marker = member["metadata"][0]["value"][0]["resource"]["marker"]
    marker["@id"] = anno_id

    member_map[anno_id] = marker # member

    member_id_spl = member_id.split("#xywh=")
    canvas_id = member_id_spl[0]

    if canvas_id not in canvas_map:
      canvas_map[canvas_id] = []
    canvas_map[canvas_id].append(member)

  canvas_text_map = {}

  for canvas_id in canvas_map:
    # 最初のノードを取得する
    start_node_id = None

    for member in canvas_map[canvas_id]:
      marker = member["metadata"][0]["value"][0]["resource"]["marker"]

      if "prev_line" not in marker and "next_line" in marker:
        start_node_id = marker["@id"]
        break

    # print(start_node_id)

    if not start_node_id:
        continue
    
    # IIIFキュレーションリストを再起的に処理する
    data = [""]
    def handle(node_id, line_index):
      node = member_map[node_id]
      data[line_index] += node["text"]

      if "next" in node:
        handle(node["next"], line_index)

      if "next_line" in node:
        data.append("")
        line_index += 1
        handle(node["next_line"], line_index)

    handle(start_node_id, 0)

    canvas_text_map[canvas_id] = data

  return canvas_text_map

tmp_path =  "data/text/" + file_id + "/text.json.gzip"

with gzip.open(tmp_path, 'r') as f:
  df = json.load(f)

selections = df["selections"]

output = []

for selection in selections:
  members = selection["members"]
  manifest = selection["within"]["@id"]
  pages, images = getManifestData(manifest)
  label = selection["within"]["label"]

  ######

  canvas_text_map = getCanvasTextMap(members)

  #####
  
  map = {}

  index = 1

  for member in members:

      member_id = member["@id"]

      member_id_spl = member_id.split("#xywh=")

      canvasId = member_id_spl[0]

      # 要検討
      if canvasId not in canvas_text_map:
          continue

      page = pages[canvasId]
      
      hash = hashlib.md5(canvasId.encode('utf-8')).hexdigest()

      if canvasId not in map:
          map[canvasId] = {
              "objectID" : hash,
              "attribution" : attribution,
              "target" : target,
              # "vol_str" : '{} {}'.format(str(vol).zfill(2), config_map[vol]),
              "vol" : vol,
              "label": canvas_text_map[canvasId],
              "image" : images[canvasId],
              "work" : label,
              "page" : page,
              "pos" : index,
              # "curation" : curationUrl,
              "manifest" : manifest,
              "canvas" : canvasId,
              # "koui" : [],
              "type" : "コマ",
              "text": "\n".join(canvas_text_map[canvasId]),
              "name": name
          }

          index += 1

  for canvas in map:
      obj = map[canvas]
      output.append(obj)

# opath = root + "/output/" + file_id + "/map.json"

opath = "data/text/{}/map.json".format(file_id)
os.makedirs(os.path.dirname(opath), exist_ok=True)

with open(opath, 'w') as outfile:
    json.dump(output, outfile, ensure_ascii=False,
                indent=4, sort_keys=True, separators=(',', ': '))