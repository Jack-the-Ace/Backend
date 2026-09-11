# 게시글 저장 웹 애플리케이션 개발
# entity(테이블) 2개 RDBMS
# 1. board(no, title, message, user_id, hits, created_at).. PK(no)
# 2. board_image(no, board_no, image_url).. PK(no),FK(board_no)

# MYSQL DBMS 를 실행하여 터미널에서 CLI로 - 테이블 생성 쿼리 실행 -----------------------------
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
#-----------------------------------------------------------------------------------------------

# Fast API를 이용하여 REST API 구축하기

#1. FastAPI 앱 객체 생성
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel, Field
app= FastAPI()

# DBMS 접속 기능을 가진 모듈 사용
from db import get_connection

# ---------------------------------------------------------------------------------------------
# 게시글 목록 조회 (READ) -- 전체 게시글 요청
# ---------------------------------------------------------------------------------------------
@app.get('/boards')
def get_all_boards():
    # board 테이블에 있는 데이터들 불러오기 -- MySQL DBMS와 연결을 매번 하기 짜증. 별도의 파일(db.py)에 기능을 만들고 모듈로서 재사용
    #1) DBMS 연결 및 쿼리문 실행객체 cursor 얻어오기
    db= get_connection()
    cursor= db.cursor()

    #2) 모든 데이터를 불러오는 쿼리문 수행 및 데이터 가져오기
    sql= "SELECT * FROM board ORDER BY no DESC"  #최신글이 먼저 보이도록 no의 내림차순
    cursor.execute(sql)
    rows= cursor.fetchall()

    #3) 요청 작업이 끝났으니 DBMS와 연결 종료
    db.close()

    #4) 읽어온 모든 게시글 데이터 row를 JSON형식으로 만들어서 리턴(클라이언트에게 응답)
    return rows  # fastapi는 dict 타입의 파이썬데이터를 자동으로 json string 으로 변환하여 응답해줌

# 터미널에서 fast api 애플리케이션을 실행해주는 웹서버(uvicorn)를 실행하기!
#  uvicorn main:app --reload  로 실행!


class BoardInput(BaseModel):
    title: str = Field(min_length=1, max_length=255)
    message: str
    user_id: str = Field(min_length=1, max_length=50)
    image_urls: list[str] = Field(default_factory=list)


@app.post('/boards', status_code=201)
def create_board(board: BoardInput):
    db = get_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute(
                'INSERT INTO board (title, message, user_id) VALUES (%s, %s, %s)',
                (board.title, board.message, board.user_id),
            )
            board_no = cursor.lastrowid
            if board.image_urls:
                cursor.executemany(
                    'INSERT INTO board_image (board_no, image_url) VALUES (%s, %s)',
                    [(board_no, url) for url in board.image_urls],
                )
        db.commit()
        return {'no': board_no}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.get('/boards/{board_no}')
def get_board(board_no: int):
    db = get_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT * FROM board WHERE no = %s', (board_no,))
            board = cursor.fetchone()
            if board is None:
                raise HTTPException(status_code=404, detail='Board not found')
            cursor.execute(
                'SELECT * FROM board_image WHERE board_no = %s ORDER BY no',
                (board_no,),
            )
            board['images'] = cursor.fetchall()
            return board
    finally:
        db.close()


@app.put('/boards/{board_no}')
def update_board(board_no: int, board: BoardInput):
    db = get_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute('SELECT no FROM board WHERE no = %s FOR UPDATE', (board_no,))
            if cursor.fetchone() is None:
                raise HTTPException(status_code=404, detail='Board not found')
            cursor.execute(
                'UPDATE board SET title = %s, message = %s, user_id = %s WHERE no = %s',
                (board.title, board.message, board.user_id, board_no),
            )
            cursor.execute('DELETE FROM board_image WHERE board_no = %s', (board_no,))
            if board.image_urls:
                cursor.executemany(
                    'INSERT INTO board_image (board_no, image_url) VALUES (%s, %s)',
                    [(board_no, url) for url in board.image_urls],
                )
        db.commit()
        return {'no': board_no}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


@app.delete('/boards/{board_no}', status_code=204)
def delete_board(board_no: int):
    db = get_connection()
    try:
        with db.cursor() as cursor:
            cursor.execute('DELETE FROM board WHERE no = %s', (board_no,))
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail='Board not found')
        db.commit()
        return Response(status_code=204)
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()

