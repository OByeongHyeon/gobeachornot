import requests
import json
from urllib import parse
url = 'http://apis.data.go.kr/1192000/service/OceansBeachSeawaterService1/getOceansBeachSeawaterInfo1'
key = 'JczkNAYUK0nuC7gzVNgSj2%2FUHiwakF7h%2BMI7BkHeAuKc7ctuY961tl%2F%2B%2Fo2hCS2TjorkkeQ2IEek%2BGPFiC0Xdg%3D%3D'

name = '관성솔밭'

a = {}

for i in range(2018,2013,-1):
    queryParams = f'?{parse.quote_plus("ServiceKey")}={key}&' + parse.urlencode({
        parse.quote_plus('resultType'): 'json',
        parse.quote_plus('SIDO_NM'): '전남',
        parse.quote_plus('RES_YEAR'): i})
    req = requests.get(url + queryParams)
    d = req.json()['getOceansBeachSeawaterInfo']['item']

    for j in d:
        print(j)
        if j['sta_nm'] == name:
            a['대장균'] = j['res1']
            a['장구균'] = j['res2']
            a['적합여부'] = j['res_yn']
            a['조사지점(위도)'] = j['lat']
            a['조사지점(경도)'] = j['lon']
            break
    if a!={}:
        break
    if a=={} and i==2014:
        a['대장균'] = d[0]['res1']
        a['장구균'] = d[0]['res2']
        a['적합여부'] = d[0]['res_yn']
        a['조사지점(위도)'] = d[0]['lat']
        a['조사지점(경도)'] = d[0]['lon']

print(a)

# print(json.dumps(request.json(), indent=4, ensure_ascii = False))


