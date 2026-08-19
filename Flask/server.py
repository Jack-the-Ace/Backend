#0. flask 모듈 설치
# pip install flask

#1. flask 모듈에서 Flask 클래스 불러오기
from flask import Flask

#2. Flask 객체 생성
app= Flask(__name__)  #현재 실행중인 모듈의 이름을 파라미터로 전달

#3. root 경로 - 웹의 진입점
@app.route('/')
def hello():  #함수명은 마음대로...
    return "Hello Flask Root!"  #응답

#5. 특정 경로 지정
@app.route('/users')
def get_users():
    return 'This is all user list'

#6. post 방식 요청
@app.route('/users', methods=['POST'])
def post_users():
    return 'POST user!!!!'

#7. 여러 요청 메소드를 한번에 받아 분기처리
from flask import request
@app.route('/boards', methods=['GET','POST'])
def board():
    if request.method=='GET':
        return 'board GET request'
    elif request.method=='POST':
        return 'board POST request'

#8. 파라미터 받기
#1) GET 방식으로 전달된 요청 파라미터
@app.route('/test', methods=['GET'])
def get_test():
    name= request.args.get('name')
    message= request.args.get('msg')
    return f"{name}:{message}"

#2) POST 방식으로 전달된 요청 데이터 받기
@app.route('/test', methods=['POST'])
def post_test():
    name= request.form.get('name')
    message= request.form.get('msg')
    return f"{name} <br> {message}"

#9. 서브 경로 사용하기
@app.route('/notes', methods=['GET'])
def get_all_notes():
    return "all note data"

@app.route('/notes/<no>', methods=['GET'])
def get_note(no):
    return f"note {no}번"

# 서브경로 + 요청 파라미터
@app.route('/notes2/<no>', methods=['GET'])
def get_note2(no):
    title= request.args.get('title')
    return f"note {no}번 - {title}"

# 서브경로 + POST + 데이터
@app.route('/notes2/<title>', methods=['POST'])
def post_note(title):
    message= request.form.get('msg')
    return f"{title} ~ {message}"
#동작안될것임. why? CORS 정책에 의해 다른 도메인에는 접근 불가.

#(해결)
#방법1 : 사용자가 사용하는 프론트엔드 HTML페이지를 flask 웹서버에서 호스팅하기
#방법2 : 백엔드 애플리케이션에서 CORS 허용 설정. -- FastAPI 수업에서 소개

#방법1로 해결하기
from flask import render_template
@app.route('/html')
def html():
    return render_template('index.html')  #render_template() 함수는 기본적으로 프로젝트폴더의 templates라는 폴더에서 파일을 찾음.


#RESTful API
#C: CREATE
@app.route('/posts', methods=['POST'])
def save_data():
    #여기서 DB작업 해야 함.
    title= request.form.get('title')
    return f"{title}: POST!"

#R: READ
@app.route('/posts', methods=['GET'])
def all_data():
    return f"all data get"

@app.route('/posts/<no>', methods=['GET'])
def get_data(no):
    return f"{no}번 data get"

#U: Update
@app.route('/posts/<no>', methods=['PUT'])
def update_data(no):
    return f"{no}번 data update"

#D: Delete
@app.route('/posts/<no>', methods=['DELETE'])
def delete_data(no):
    return f"{no}번 data delete"

#CRUD 테스트를 html로 만들기 짜증.. 그래도 등장한 Request용 도구들 중 postman 사용

#----------------------------------------------------------------------------------------------------------------------------------------------
#4. 웹앱 실행하기..
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)  #같은 네트워크의 다른 어떤 컴퓨터든(특수IP: 0.0.0.0) 접속 허용

