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


# TODO : CRUD 작업 완성!!!

