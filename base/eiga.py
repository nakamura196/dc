import os
import requests
import time

code = 1

flg = True

while flg:
    url = "http://www.genji.co.jp/eiga-sub.php?code={}&file=eiga-all.txt".format(code)

    path = "data/eiga/" + str(code).zfill(8) + ".html"

    if not os.path.exists(path):

        print(code)

        time.sleep(1)

        response = requests.get(url)
        response.encoding = response.apparent_encoding

        with open(path, 'w') as file:
            file.write(response.text)

    code += 1

    if code > 30000:
        break