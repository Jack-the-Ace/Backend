# Python 에서 MySQL DBMS와 연동하기

#0. MySQL DBMS와 연결하는 기능을 제공하는 외부모듈 pymysql 설치
# pip install pymysql

#1. 모듈 사용
import pymysql

#2. MySQL DBMS와 연결 (Database 매니지먼트 시스템)
db= pymysql.connect(host='127.0.0.1', port=3306, user='jack', password='1234', database='mbca', charset='utf8mb4')

#3. SQL 쿼리문을 수행해주는 Cursor 객체 생성
cursor= db.cursor()

#7. 쿼리 요청 결과를 튜플이 아니라 딕셔너리로 받기
cursor= db.cursor(pymysql.cursors.DictCursor)

#4. 원하는 쿼리문 작성 및 cursor 객체를 이용하여 쿼리문 실행
sql= 'SELECT * FROM BOOK'
cursor.execute(sql)

#5-A. (SELECT)인 경우 -- 결과표에서 데이터 추출
# 1) 모든 레코드(row) 가져오기
rows = cursor.fetchall()  #결과를 2차원 튜플(tuple)로 줌
print(rows)
print()

# 2) 한 줄 단위로 가져오기 -- 위에서 fetchall()을 하면 이미 커서가 가장 아래로 내려온 상태임. 그래서 결과표를 다시 요청
sql= 'SELECT * FROM BOOK'
cursor.execute(sql)

row= cursor.fetchone()
print(row)
print(cursor.fetchone())
print(cursor.fetchone())
print(cursor.fetchone())
print()

# 3) 여러줄 가져오기 (size: 개수 지정)
rows= cursor.fetchmany(3)  # 3줄 가져오기
print(rows)
print()

# 4) WHERE 절 사용한 쿼리문
sql= 'SELECT * FROM BOOK WHERE BOOK_ID=4'
cursor.execute(sql)
row= cursor.fetchone()
print(row)

# 5-B. (INSERT, UPDATE, DELETE)인 경우 - DBMS에 쿼리 작업(트렌잭션)을 완료하도록.
db.commit()

#6) DBMS와의 연결종료
db.close() 
