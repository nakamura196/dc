import os
import requests
import time

code = 1

flg = True

while flg:
    url = "http://www.genji.co.jp/ise-sub.php?code={}&file=ise.txt".format(code)

    path = "data/ise/" + str(code).zfill(8) + ".html"

    if True or not os.path.exists(path):

        print(code)

        time.sleep(1)

        response = requests.get(url)
        response.encoding = response.apparent_encoding

        with open(path, 'w') as file:
            file.write(response.text)

    code += 1