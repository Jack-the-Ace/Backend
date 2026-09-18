# 게시글 저장 웹 애플리케이션 개발
# entity(테이블) 2개 RDBMS
# 1. board(no,title,message,user_id,hits,created_at).. PK(no)
# 2. board_image(no,board_no,image_url).. PK(no),FK(board_no)

# MYSQL DBMS를 실행하여 터미널에서 CLI로 - 테이블 생성 쿼리 실행 -----------
create_sql='''
CREATE TABLE board(
    no INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    message TEXT,
    user_id VARCHAR(50),
    hits INT DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE board_image(
    no INT AUTO_INCREMENT PRIMARY KEY,
    board_no INT,
    image_url VARCHAR(500),
    FOREIGN KEY(board_no) REFERENCES board(no) ON DELETE CASCADE
);
'''
#--------------------------------------------------------------------

# Fast API 를 이용하여 REST API 구축하기

#1. FastAPI 앱 객체 생성
from fastapi import FastAPI
app= FastAPI()

# DBMS 접속기능을 가진 모듈 사용
from db import get_connection

# ---------------------
# 게시글 목록 조회 (READ) -- 전체 게시글 요청
# ---------------------
@app.get('/boards')
def get_all_boards():
    # board 테이블에 있는 데이터들 불러오기 -- MySQL DBMS와 연결을 매번하기 짜증. 별도의 파일(db.py)에 기능을 만들고 모듈로서 재사용

    #1) DBMS 연결 및 쿼리문 실행객체 cursor 얻어오기
    db= get_connection()
    cursor= db.cursor()

    #2) 모든 데이터를 불러오는 쿼리문 수행 및 데이터 가져오기
    sql= "SELECT * FROM board ORDER BY no DESC" #최신글이 먼저 보이도록 no의 내림차순
    cursor.execute(sql)
    rows= cursor.fetchall()

    #3) 요청 작업이 끝났으니 DBMS와 연결 종료
    db.close()

    #4) 읽어온 모든 게시글 데이터 rows를 JSON형식으로 만들어서 리턴(클라이언트에게 응답)
    return rows # fastapi는 dict 타입의 파이썬데이터를 자동으로 json string 으로 변환하여 응답해줌

# 터미널에서 fast api 애플리케이션을 실행해주는 웹서버(uvicorn)를 실행하기!
# uvicorn main:app --reload 로 실행


# ---------------------
# 게시글 상세 조회 (READ) -- 게시글 한개를 가져오는 요청
# ---------------------
@app.get('/boards/{board_no}')
def get_board(board_no:int):  # subpath의 값을 파라미터로 받음
    #1) DB 연결
    db= get_connection()
    cursor= db.cursor()

    #2) 쿼리문 실행(조회수+1, 게시글 내용, 이미지 조회) ~~ 게시글과 이미지 조회는 JOIN으로 수행할 수도 있겠지만..
    #조회수 증가
    sql="""UPDATE board SET hits= hits+1 WHERE no=%s"""
    cursor.execute(sql, (board_no))

    #게시글 조회
    cursor.execute('SELECT * FROM board WHERE no=%s', (board_no))
    board= cursor.fetchone()

    #첨부파일 이미지들 조회
    cursor.execute('SELECT * FROM board_image WHERE board_no=%s', (board_no))
    images= cursor.fetchall()

    db.commit()
    db.close()

    # 사용자에게 게시글 내용과 이미지를 응답해주기.. 단, 구분을 편하게 하기 위해 key를 지정
    return {'board':board, 'images':images}

# ---------------------
# 게시글 생성, 저장 (CREATE) -- 게시글 저장하는 기능
# ---------------------
from fastapi import Form, File, UploadFile

# 업로드된 파일이 저장될 경로.. 없다면 만들어지도록..
import os
UPLOAD_FOLDER= 'uploads/'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)  # exist_ok=True : 이미 해당 이름의 폴더가 있다면 만들지 말고 명령을 무시해라.

# 사용자가 보낸 원본 파일명에 특수문자 같은 것이 포함되어 있으며 파일입출력할때 문제생김
# 이를 알아서 이쁘게 수정해주는 도구 모듈 사용
from werkzeug.utils import secure_filename
from datetime import datetime

@app.post('/boards')
async def insert_board(title:str=Form(...), message:str=Form(...), user_id:str=Form(...), images:list[UploadFile]= File(default=[])):   # 사용자가 보내온 데이터를 받기  /  (...='갈(오렌지)색'을 반드시 받아야한다, 공백X) /  'default=' 는 생략가능
    #DBMS 접속
    db= get_connection()
    cursor= db.cursor()

    #1) 게시글 저장(board 테이블)
    cursor.execute("""INSERT INTO board(title, message, user_id) VALUES(%s,%s,%s)""", (title, message, user_id))  # %s=여기에 str이 올꺼야(d,b=숫자,불린)

    # 첨부이미지파일들을 별도의 테이블에 저장하기 위해 insert로 삽입된 게시글의 번호 필요
    board_no= cursor.lastrowid

    #2) 업로드된 파일들을 저장(board_image 테이블)
    for file in images:
        # 파일이 실제로 존재하는지 확인
        if file.filename:
            # 원본 파일명을 이쁘게....
            original_filename= secure_filename(file.filename)

            # 파일명 중복 방지를 위한 날짜와 시간 정보를 파일명에 활용
            timestamp= datetime.now().strftime("%Y%m%d%H%M%S%f")  #2026091811164011111 밀리세컨드=%f
            filename= f"{timestamp}_{original_filename}"  # "2026091811164011111_aa.png"  <-- 파일명

            # 업로드된 파일을 저장할 경로와 파일명 결합
            filepath= os.path.join(UPLOAD_FOLDER, filename)

            # 만들어진 경로/파일명 에 이미지파일 데이터를 저장
            with open(filepath, 'wb') as f:
                # contents= file.read(1024 * 1024)  # 1MB씩 읽기 
                # while contents:
                #     f.write(contents)
                #     contents= file.read(1024*1024)

                # 위 작업을 간결하게..
                while contents := await file.read(1024*1024):     # async - await
                    f.write(contents)

            # DB에 파일 경로 저장
            cursor.execute("""INSERT INTO board_image(board_no, image_url) VALUES(%s,%s)""", (board_no, filepath))

    # DB 반영
    db.commit()
    db.close()

    # 사용자에게 응답
    return {'message':'insert board data'}

    

# ---------------------
# 게시글 수정 (UPDATE) -- 게시글 수정하는 기능, 수정할 데이터도 파라미터로 받기
# ---------------------
@app.put('/boards/{board_no}')
def update_board(
    board_no:int,
    title:str= Form(...),
    message:str= Form(...),
    user_id:str= Form(...),
    images:list[UploadFile]= File(default=[])
    ):  

    #DBMS 접속
    db= get_connection()
    cursor= db.cursor()

    #게시글 수정 (board테이블)
    cursor.execute("""UPDATE board SET title=%s, message=%s WHERE no=%s""", (title, message, board_no))

    #기존 이미지 정보 삭제(board_image테이블)
    cursor.execute("""DELETE FROM board_image WHERE board_no=%s""", (board_no))

    #새로 업로드된 첨부파일이 있다면 저장 및 DB에 등록
    for file in images:
        if file.filename:
            original_filename= secure_filename(file.filename)
            timestamp= datetime.now().strftime("%Y%m%d%H%MS%f")
            filename= f"{timestamp}_{original_filename}"
            filepath= os.path.join(UPLOAD_FOLDER, filename)

            with open(filepath,"wb") as f:
                while contents := file.file.read(1024*1024):
                    f.write(contents)

            #DB에 첨부파일 등록(저장)
            cursor.execute("""INSERT INTO board_image(board_no, image_url) VALUES(%s,%s)""", (board_no, filepath))

    #DB 반영
    db.commit()
    db.close()
    return {'message':'updated'}

# ---------------------
# 게시글 삭제 (DELETE) -- 게시글 삭제 기능
# ---------------------
@app.delete('/boards/{board_no}')
def delete_board(board_no:int):  
    db= get_connection()

    try:
        with db.cursor() as cursor:
            cursor.execute("DELETE FROM board WHERE no=%s", (board_no))

        db.commit()
        return {'message':'board deleted'}

    finally:
        db.close()



# Frontend (React 요청 코드) sample

# const fromData= new FormData();   // 빈 택배상자 만들기
# formData.append('title','hello');
# formData.append('message', 'nice to meet you');
# formData.append('user_id','sam')

# for(let i=0; i<file.length; i++){
#     formData.append('images', files[i]);
# }

# fetch("/boards", {method:'POST', body: formData}).then().then()


