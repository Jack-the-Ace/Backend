from fastapi import FastAPI
app=FastAPI()

@app.get('/')
def aaa():
    return "Hello FFFFFFast~~API~~"

@app.get('/aaa')
def get_users():
    return "This is 'AAAAAA' man~"

@app.post('/aaa')
def post_users():
    return "이것은 'AAAAAA' 맨~"

from fastapi import Request
@app.api_route('/bbb', methods=['GET','POST'])
def board(request:Request):
    if request.method == 'GET':
        return "board GET - bbb 겟!"
    elif request.method == 'POST':
        return "board POST - bbb 포스트!"

@app.get('/test')
def test_get(name:str, msg:str):
    return {'method':'GET', 'name':name, 'message':msg}

from fastapi import Form
@app.post('/test')
def test_post(name:str= Form(), msg:str= Form(...)):
    return {'method':'POST', 'name':name, 'message':msg}

@app.post('/test2')
def test_post(name:str= Form('이름없음'), msg:str= Form('내용없음')):
    return {'method':'POST', 'name':name, 'message':msg}

@app.get('/notes/{no}')
def notes(no:int):
    return {'method':'GET', '서브경로':no}

@app.get('/notes2/{no}')
def notes2(no:int, name:str, msg:str):
    return {'method':'GET', '서브경로':no, '이름':name, '메세지':msg}

@app.post('/notes/{no}')
def post_note(no:int, title:str= Form(...), msg:str= Form(...)):
    return {'method':'POST', '서브경로':no, '제목':title, '메세지':msg}

from fastapi.responses import HTMLResponse
@app.get('/html')
def html():
    with open('./Note.html', 'r', encoding='utf-8') as f:
        html_content= f.read()
    return HTMLResponse(content=html_content, status_code=200)

from fastapi.responses import FileResponse
@app.get('/html2')
def html2():
    return FileResponse('./Note.html')

@app.get('/image')
def image():
    return FileResponse('./images/newyork.jpg')

from fastapi.staticfiles import StaticFiles
app.mount('/reactapp', StaticFiles(directory='frontend/dist', html=True), name='React Index Page~')

@app.get('/reactapp')
def react():
    return FileResponse('./frontend/dist/index.html')

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://127.0.0.1:5500','http://localhost:5173'],
    allow_methods=['*'],
    allow_headers=['*'],
)
@app.post('/json')
def json_post(data:dict):
    userid= data['userid']
    message= data['msg']
    return f"아이디: {userid} / 메세지: {message}"