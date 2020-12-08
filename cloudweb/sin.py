import requests
import json
url2 = 'https://seantour.com/seantour_map/travel/getBeachCongestionApi.do'

name = '중문색달'

req = requests.get(url2)

data = req.json()

print(data)

r = {}

for i in data:
    nm = data[i]['poiNm'].split(' ')[1]
    if nm in name or name in nm:
        print(nm)
        print(name)
        r['uniqPop'] = data[i]['uniqPop']
        r['congestion'] = data[i]['congestion']
        break

print(r)
