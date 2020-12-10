from flask import Flask, render_template, request, redirect, url_for
import requests
import pandas as pd
from urllib import parse
import pymongo
from bson.json_util import dumps


url1 = 'http://apis.data.go.kr/1192000/service/OceansBeachSeawaterService1/getOceansBeachSeawaterInfo1'
key1 = 'JczkNAYUK0nuC7gzVNgSj2%2FUHiwakF7h%2BMI7BkHeAuKc7ctuY961tl%2F%2B%2Fo2hCS2TjorkkeQ2IEek%2BGPFiC0Xdg%3D%3D'
url2 = 'https://seantour.com/seantour_map/travel/getBeachCongestionApi.do'
url3 = 'http://apis.data.go.kr/1192000/service/OceansBeachInfoService1/getOceansBeachInfo1'
key2 = 'JczkNAYUK0nuC7gzVNgSj2%2FUHiwakF7h%2BMI7BkHeAuKc7ctuY961tl%2F%2B%2Fo2hCS2TjorkkeQ2IEek%2BGPFiC0Xdg%3D%3D'

app = Flask(__name__)

@app.route('/')
def index():
    return redirect(url_for('main'))


@app.route('/main',methods = ['POST','GET'])
def main():
    if request.method == 'POST':
        fil = request.form
        print(fil)
        f = pd.read_csv('해양수산부_해수욕장 개장 폐장 정보.csv', encoding = 'CP949', engine='python')

        sido = f['시도 주소'] == fil['sido']
        sigun = f['시군구 주소'] == fil['sigun']

        if fil['sido'] != "none" and fil['sigun'] != "none":
            data = f[sido & sigun][['해수욕장명','개장일','폐장일','홈페이지','연락처']]
        elif fil['sigun'] == "none":
            data = f[sido][['해수욕장명', '개장일', '폐장일', '홈페이지', '연락처']]
        else :
            data = f[sigun][['해수욕장명','개장일','폐장일','홈페이지','연락처']]

        key = data.to_dict().keys()
        v = data.to_dict().values()
        v = list(map(lambda x:list(x.values()), v))
        value=[]

        for i in range(5):
            d = {j:v[i][j] for j in range(len(v[i]))}
            value.append(d)

        result = dict(zip(key, value))
        result['시도 주소'] = fil['sido']
        result['시군구 주소'] = fil['sigun']

        return render_template('main.html',result = result)
    if request.method == 'GET':
        return render_template('main.html')

@app.route('/detail')
def detail():

    sido_map = {'부산광역시':'부산','인천광역시':'인천','울산광역시':'울산','강원도':'강원','충청남도':'충남'
               ,'전라북도':'전북','전라남도':'전남','경상북도':'경북','경상남도':'경남','제주특별자치도':'제주'}

    name = request.args.get('name')
    sido = sido_map[request.args.get('sido')]


    f = pd.read_csv('해양수산부_해수욕장 개장 폐장 정보.csv', encoding='CP949', engine='python')
    data = f[f['해수욕장명'] == name].to_dict()

    result = {}
    key = list(data['연번'])[0]

    result['해수욕장명'] = data['해수욕장명'][key]
    result['주소'] = data['시도 주소'][key] + " " + data['시군구 주소'][key] + " " + data['읍면동 주소'][key]
    if data['이하 주소'][key] != "-":
        result['주소'] = result['주소'] + " " + data['이하 주소'][key]
    result['개장일'] = data['개장일'][key]
    result['폐장일'] = data['폐장일'][key]
    result['주요행사'] = ""
    for i in range(1, 9):
        s = '주요행사' + str(i)
        if data[s][key] != "-":
            result['주요행사'] = result['주요행사'] + data[s][key] + ", "
        if i == 8:
            result['주요행사'] = result['주요행사'][:-2]
    result['홈페이지'] = data['홈페이지'][key]
    result['연락처'] = data['연락처'][key]

    tmp = {}

    for i in range(2018, 2013, -1):
        queryParams = f'?{parse.quote_plus("ServiceKey")}={key1}&' + parse.urlencode({
            parse.quote_plus('resultType'): 'json',
            parse.quote_plus('SIDO_NM'): sido,
            parse.quote_plus('RES_YEAR'): i})
        req = requests.get(url1 + queryParams)
        d = req.json()['getOceansBeachSeawaterInfo']['item']

        for j in d:
            if j['sta_nm'] == name:
                tmp['대장균'] = j['res1']
                tmp['장구균'] = j['res2']
                tmp['적합여부'] = j['res_yn']
                tmp['조사지점(위도)'] = j['lat']
                tmp['조사지점(경도)'] = j['lon']
                break
        if tmp != {}:
            break
        if tmp == {} and i == 2014: #TODO: 수정?
            tmp['대장균'] = d[0]['res1']
            tmp['장구균'] = d[0]['res2']
            tmp['적합여부'] = d[0]['res_yn']
            tmp['조사지점(위도)'] = d[0]['lat']
            tmp['조사지점(경도)'] = d[0]['lon']

    result.update(tmp)

    req = requests.get(url2)

    data = req.json()

    for i in data:
        nm = data[i]['poiNm'].split(' ')[1]
        if nm in name or name in nm:
            result['uniqPop'] = data[i]['uniqPop']
            result['congestion'] = data[i]['congestion']
            break

    if 'uniqPop' not in result:
        result['uniqPop'] = '미측정'
        result['congestion'] = '미측정'

    if result['congestion'] == '3' and result['적합여부'] == '부적합':
        result['휴양적합여부'] = '부적합1'
    elif result['congestion'] == '2' and result['적합여부'] == '부적합':
        result['휴양적합여부'] = '부적합2'
    else: result['휴양적합여부'] = '적합'



    queryParams = f'?{parse.quote_plus("ServiceKey")}={key2}&' + parse.urlencode({
        parse.quote_plus('resultType'): 'json',
        parse.quote_plus('SIDO_NM'): sido})
    data3 = requests.get(url3 + queryParams).json()['getOceansBeachInfo']['item']

    for i in data3:
        if i['sta_nm'] in name or name in i['sta_nm']:
            result['beach_wid'] = i['beach_wid']
            result['beach_len'] = i['beach_len']
            result['beach_knd'] = i['beach_knd']
            result['lat'] = i['lat']    #TODO: 쓸지안쓸지
            result['lon'] = i['lon']
            break

    # print(render_template('detail.html',result=result))
    return render_template('detail.html',result=result)

@app.route('/login',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        info = request.form
        print(info)



    return render_template("login.html")

@app.route('/checkid',methods = ['POST'])
def checkid():
    if request.method == 'POST':
        info = request.form

        db = client.gobeachornot
        col = db.signup

        query = {"id":info["id"], "pw":info["pw"]}

        cur = col.find(query)
        doc = dumps(list(cur))

        if doc != "[]":
            return render_template("mybeach.html")


        return render_template("login.html")



@app.route('/mybeach')
def mybeach():

    db = client.gobeachornot
    col_list = db.collection_names()
    # col = db.signup
    print(col_list)

    return render_template("login.html")

@app.route('/signup',methods = ['POST','GET'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    if request.method == 'POST':
        db = client.gobeachornot
        col = db.signup

        tmp = request.form

        if tmp['id']=="" or tmp['pw']=="" or tmp['name']=="" or tmp['hp']=="":
            message = "빈칸 없이 모두 작성 부탁드립니다."
            return render_template("signup.html", message=message)

        info = {'id':tmp['id'], 'pw':tmp['pw'], 'name':tmp['name'], 'hp':tmp['hp']}
        col.insert_one(info)

        return render_template("login.html")



if __name__ == '__main__':
    app.run(debug=True)







#
# f = open('해양수산부_해수욕장 개장 폐장 정보.csv', 'r')
# rdr = csv.reader(f)
# for line in rdr:
#     print(line)
# f.close()
