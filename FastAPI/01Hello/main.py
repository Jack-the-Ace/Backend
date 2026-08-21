#0. fastapi 모듈, uvicorn 모듈 설치
# pip install fastapi uvicorn

#1. FastAPI import
from fastapi import FastAPI

#2. FastAPI 객체 생성
app= FastAPI()

#3. root 경로 - 웹의 진입점
@app.get('/')
def aaa():
    return "Hello FastAPI root"  #사용자에게 응답 response ~ 기본 응답 Content-Type:application/json

#4. 이 서버의 실행
# flask 처럼 웹서버 기능이 없기에 ASGI인 uvicorn 을 이용하여 FastAPI app을 실행
# 터미널에서 실행.  --  [01Hello폴더에서> uvicorn main:app --reload  ]

# [FastAPI의 장점]
# API 명세서 문서를 자동으로 만들어줌. [ http://127.0.0.1:8000/docs ] (Swagger UI), (redoc)도 있음

#라우팅
#5. /users 경로 - GET 요청 처리
@app.get('/users')
def get_users():
    # 이 곳에서 DB에 있는 사용자 정보를 읽어와서 응답!
    return "This is all user list"

#6. /users 경로 - POST 요청 처리
@app.post('/users')
def post_user():
    return "User post! 한글도 되나??"

#7. 요청 메소드 상관없이 대응하는 경로: 해당 경로의 모든 요청을 받아 분기 처리
from fastapi import Request
@app.api_route('/boards', methods=['GET','POST'])
def board(request: Request):  #사용자 요청에 관련된 정보를 파라미터로 받음
    #요청에 따라 분기 처리
    if request.method == 'GET':
        return "board GET"
    elif request.method == 'POST':
        return "board POST"

#8. 요청 파라미터 처리: GET 방식으로 요청시 쿼리스트링으로 전달되는 요청 파라미터 처리
# 1) GET 방식 : ?name=sam&msg=Hello world
@app.get('/test')
def test_get(name:str, msg:str):  #요청 파라미터에 전달된 값을 매개변수로 받으면 됨
    return {'method':'GET', 'name':name, 'message':msg}

# 2) POST 방식 : 요청파라미터가 form-data 형식으로 전달되기에.. 이를 받기
from fastapi import Form
@app.post('/test')
def test_post(name:str= Form(), msg:str= Form(...)):  # ... : 필수 파라미터 라는 의미
    return {'method':'POST', 'name':name, 'message':msg}

#요청데이터를 보내지 않으면 에러. 그래서, 보내지 않았을때의 기본값 부여
@app.post('/test2')
def test_post(name:str= Form('익명'), msg:str= Form('냉무')):
    return {'method':'POST', 'name':name, 'message':msg}


#9. 서브경로 받기
@app.get('/notes/{no}')  # {no} 자리에는 사용자가 원하는 값으로 경로 지정
def notes(no:int):  #파라미터로 서브경로 값 받기  (타입힌트도 적용됨)
    return {'method':'GET', '서브경로':no}

#10. 서브경로 + 쿼리 스트링  ?name=sam&msg=Hello
@app.get('/notes2/{no}')  # {no} 자리에는 사용자가 원하는 값으로 경로 지정
def notes2(no:int, name:str, msg:str):  #파라미터로 서브경로 값, 쿼리스트링 받기  (타입힌트도 적용됨)
    return {'method':'GET', '서브경로':no, '이름':name, '메세지':msg}

#11. 서브경로 + POST data
@app.post('/notes/{no}')
def post_note(no:int, title:str=Form(...), msg:str=Form(...)):
    return {'method':'POST', '서브경로':no, '제목':title, '메세지':msg}
# index.html 에서 JS의 AJAX 기술로 데이터를 보내기
# JS에서 다른 서버의 도메인에 요청하면 CORS 정책 문제로 전달되지 않음.

# (해결)
#방법1. 사용자가 사용하는 프론트엔드 HTML 페이지를 fastapi웹앱에서 실행하기
#방법2. FastAPI 설정에서 CORS 정책을 허용하도록..

#(방법1)
#12. index.html 을 fastapi에서 응답으로 보여주기 [즉, 서버에서 페이지를 그려줌. SSR]
from fastapi.responses import HTMLResponse
@app.get('/html')
def html():
    #index.html 파일을 읽어오기
    with open('./index.html', 'r', encoding='utf-8') as f:
        html_content= f.read()
    return HTMLResponse(content=html_content, status_code=200)

# 파일 읽어오는 코드 작성이 귀찮으면.. 더 쉽게 정적문서 응답 경로 만들기
from fastapi.responses import FileResponse
@app.get('/html2')
def html2():
    return FileResponse('./index.html')

# 이미지 파일 응답하기
@app.get('/image')
def image():
    return FileResponse('./images/newyork.jpg')

# react 처럼 동적으로 html 페이지를 구성하는 경우에는 추가작업 필요
from fastapi.staticfiles import StaticFiles
app.mount('/reactapp', StaticFiles(directory='frontend/dist', html=True), name='react index page')

@app.get('/reactapp')
def react():
    return FileResponse('./frontend/dist/index.html')
#------------------------------------------------------------------------------------------------------------

#(방법2) FastAPI에서 CORS 정책을 허용하도록 설정하기.
# CORS 를 허용해주는 중계자 역할의 소프트웨어 필요 - 미들웨어
#미들웨어 - 클라이언트의 요청과 서버 응답 사이에서 요청/응답을 가로채 특정 작업을 처리하는 중간 계층 소프트웨어
from fastapi.middleware.cors import CORSMiddleware
# fastapi app 에게 미들웨어를 등록해놓기.. - 보통은 처음 시작할 때 미리 해놓음.
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500','http://localhost:5173/'],  # * 쓰면 모두허용
    allow_methods=['*'],   # GET, POST 등...
    allow_headers=['*'],
    )
#--------------------------------------------------------------------------------------------------------------

# json 요청 데이터 받기
@app.post('/json')
def json_post(data:dict):  #json 요청데이터를 자동으로 fastapi가 dictionary로 변환하여 받음
    userid= data['userid'] #python의 dict 요소값 취득
    message= data['msg']
    return f"아이디: {userid} / 메세지: {message}"


