import requests
import json


url = 'http://13.125.170.17/testbus.php'

res=requests.post(url)
res.status_code
new_txt = res.text.replace("[", "")
new_txt = new_txt.replace("]", "")
new_txt = new_txt.replace('"', "")

arr_ = new_txt.split(',')

for i in arr_:
    print i

