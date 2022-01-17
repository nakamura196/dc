import os
import requests
import time

code = 1

# id = "sarashina"
# filename = "sarasina-all-4s-pl"

id = "ookagami"
filename = "ookagami"

flg = True

while flg:
    url = "http://www.genji.co.jp/{}-sub.php?code={}&file={}.txt".format(id, code, filename)

    path = "data/"+id+"/" + str(code).zfill(8) + ".html"

    if not os.path.exists(path):

        os.makedirs(os.path.dirname(path), exist_ok=True)

        time.sleep(1)

        response = requests.get(url)
        response.encoding = response.apparent_encoding

        with open(path, 'w') as file:
            file.write(response.text)

    code += 1