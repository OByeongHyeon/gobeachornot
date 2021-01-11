
## - GO BEACH OR NOT -<br><br>공공데이터를 이용한 해수욕장 방문 적합 여부 판별 서비스

### 기능
---
1. 해수욕장 검색 및 지역별 해수욕장 목록 조회
2. 각 해수욕장에 대한 기본 정보 + 연간 행사 정보 제공
3. 수질 검사 결과, 혼잡도 측정 결과를 공개하여 이를 기반으로 해당 해수욕장의 방문 적합 여부를 판별
4. 회원가입 및 로그인∙로그아웃
5. 로그인을 한 사용자에 한해 관심 해수욕장 등록·조회·삭제
<br>

### OpenAPI 방식의 공공데이터 활용 (공공데이터포털)
---
- 해수욕장 수질적합 여부 서비스 (REST)
- 해양수산부_해수욕장 혼잡도 신호등 (REST)
- 해수욕장정보 서비스 (REST)
- 해양수산부_해수욕장 개장 폐장 정보
<br>

### Total Architecture
---
<img src="https://user-images.githubusercontent.com/67847920/104159342-7a300f00-5432-11eb-81e8-a9e219beefec.png" width="700px">
### Serverless Computing & Microservice ( AWS Lambda + API Gateway )

- [Zappa](https://github.com/Miserlou/Zappa) 를 이용하여 Python Flask application을 AWS Lambda + API Gateway에 배포
- RESTful API 방식 동작

### NoSQL 기반 Data Management System ( EC2 + MongoDB )

- 회원가입 정보 + 나의 해수욕장 정보 관리
<br>

### 구현 결과
------
#### [ main ]
<img src="https://user-images.githubusercontent.com/67847920/104159429-a3e93600-5432-11eb-8971-4f246d34e8de.png" width="700px">
<img src="https://user-images.githubusercontent.com/67847920/104159440-a8155380-5432-11eb-8333-c19fe37ea5fd.png" width="700px"><br>
#### [ detail ]
<img src="https://user-images.githubusercontent.com/67847920/104159446-ab104400-5432-11eb-90de-7f750b2edcd0.png" width="700px"><br>
#### [ signup ]
<img src="https://user-images.githubusercontent.com/67847920/104159451-ad729e00-5432-11eb-84de-0809c0a5c1e2.png" width="700px"><br>
#### [ login ]
<img src="https://user-images.githubusercontent.com/67847920/104159458-afd4f800-5432-11eb-8185-94bb1ab6167a.png" width="700px">
<img src="https://user-images.githubusercontent.com/67847920/104159464-b19ebb80-5432-11eb-87b3-deaae9ec78bf.png" width="700px"><br>
#### [ my beach ]
<img src="https://user-images.githubusercontent.com/67847920/104159470-b499ac00-5432-11eb-8ecf-1e37df21aae7.png" width="700px">
