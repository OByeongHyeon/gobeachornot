import requests
import json
from urllib import parse

url3 = 'http://apis.data.go.kr/1192000/service/OceansBeachInfoService1/getOceansBeachInfo1'
key2 = 'JczkNAYUK0nuC7gzVNgSj2%2FUHiwakF7h%2BMI7BkHeAuKc7ctuY961tl%2F%2B%2Fo2hCS2TjorkkeQ2IEek%2BGPFiC0Xdg%3D%3D'

queryParams = f'?{parse.quote_plus("ServiceKey")}={key2}&' + parse.urlencode({
        parse.quote_plus('resultType'): 'json',
        parse.quote_plus('SIDO_NM'): '제주'})
req = requests.get(url3 + queryParams)
d = req.json()['getOceansBeachInfo']['item']

for j in d:
    print(j)

# print(d)