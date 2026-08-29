from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app= FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*'],
)

@app.get('/')
def hello():
    return "Pydantic Test~"

from pydantic import BaseModel
class UserData(BaseModel):
    userid:str
    msg:str
    age:int

@app.post('/json_test')
def json_test(data:UserData):
    userid= data.userid
    message= data.msg
    age= data.age
    age= age + 3
    return f"{userid} - {message} : {age}"

from fastapi.responses import PlainTextResponse
@app.get('/response_text', response_class=PlainTextResponse)
def response1():
    return '<h1>Hello. This is plain text</h1>'

from fastapi.responses import HTMLResponse
@app.get('/response_html', response_class=HTMLResponse)
def response2():
    return '<h1>Hello, This is HTML~<h1>'

from fastapi.responses import JSONResponse
@app.get('/response_json', response_class=JSONResponse)
def response3():
    return {'msg':'HELLO JSON', 'title':'제목~!'}

from fastapi.responses import RedirectResponse
@app.get('/response_redirect', response_class=RedirectResponse)
def response4():
    return RedirectResponse(url='/login')

@app.get('/login', response_class=HTMLResponse)
def login_page():
    return '<h2>로그인 페이지 입니다~!</h2>'
