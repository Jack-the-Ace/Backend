from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#1. FastAPI 앱 객체 생성
app= FastAPI()

#2. React로 만든 Frontend 웹앱의 포트번호가 달라 다른 도메인으로 인식되어 CORS 문제 발생하는 것을 방지
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=['*'],
    allow_headers=['*'],
)

#3. root 경로 지정
@app.get('/')
def hello():
    return "pydantic test"  #응답 타입을 기본적으로 json 형식으로 함

#[서버실행] 웹서버 역할을 수행하는 uvicorn 을 이용하여 실행. [ uvicorn main:app --reload ]
#4. pydantic(파이단틱) 모델을 사용하여 사용자가 요청한 데이터를 검증 및 자동 문서화
#사용자 요청 데이터 모델(구조:스키마)를 만들어 잘못된 데이터가 전달되는 것을 검증하는 기법
from pydantic import BaseModel
#사용자 요청 데이터의 모델(구조) 정의하기
class UserData(BaseModel):  #사용자 데이터의 타입을 검증해주는 기능을 가진 BaseModel을 상속
    userid:str
    msg:str
    age:int

@app.post('/json_test')
def json_test(data:UserData):  #사용자가 json 형식으로 보낸 데이터를 dictionary로 받을 수 있음.
    #사용자가 보낸 요청데이터 받기
    userid= data.userid
    message= data.msg
    age= data.age
    age= age + 1
    return f"{userid} - {message} : {age}"

#5. 서버의 응답형식을 지정하기 ~ "Content-Type:text/plain"
#1) plain text
from fastapi.responses import PlainTextResponse
@app.get('/response_text', response_class=PlainTextResponse)
def response1():
    return '<h1>Hello. This is plain text</h1>'

#2) HTML
from fastapi.responses import HTMLResponse
@app.get('/response_html', response_class=HTMLResponse)
def response2():
    return '<h1>Hello. This is html</h1>'

#3) JSON
from fastapi.responses import JSONResponse
@app.get('/response_json', response_class=JSONResponse)
def response3():
    return {'msg':'hello json', 'title':'제목'} #python의 dict 를 리턴하면 자동 json string 으로 응답

#4) redirect 응답 - 다른 경로로 요청을 다시 하도록.. 응답
from fastapi.responses import RedirectResponse
@app.get('/response_redirect', response_class=RedirectResponse)
def response4():
    #만약 로그인을 안했으면 로그인 경로로 리다이렉트 응답
    return RedirectResponse(url='/login')

@app.get('/login', response_class=HTMLResponse)
def login_page():
    return '<h2>로그인 페이지 입니다!</h2>'
