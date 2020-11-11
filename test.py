# Python 샘플 코드 #

import requests
import json
from urllib import parse
url = 'http://apis.data.go.kr/6260000/GoodPriceStoreService/getGoodPriceStore'
key = 'JczkNAYUK0nuC7gzVNgSj2%2FUHiwakF7h%2BMI7BkHeAuKc7ctuY961tl%2F%2B%2Fo2hCS2TjorkkeQ2IEek%2BGPFiC0Xdg%3D%3D'

queryParams = f'?{parse.quote_plus("ServiceKey")}={key}&' + parse.urlencode({
    parse.quote_plus('pageNo'): '1',
    parse.quote_plus('numOfRows'): '10',
    parse.quote_plus('resultType'): 'json',
    parse.quote_plus('cnCd'): '602',
    parse.quote_plus('mNm'): '김명옥',
    parse.quote_plus('sj'): '대가호',
    parse.quote_plus('localeCd'): '207'})

request = requests.get(url + queryParams)
print(json.dumps(request.json(), indent=4, ensure_ascii = False))

