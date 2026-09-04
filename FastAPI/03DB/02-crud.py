#1. mysql 과 연동하는 모듈 사용
import pymysql

#2. MySQL DBMS와 연결
db= pymysql.connect(host='127.0.0.1', user='jack', password='1234', database='mbca', charset='utf8mb4')

#3. SQL 쿼리문을 수행해주는 Cursor 객체 생성 - 결과를 dictionary로 받기
cursor= db.cursor(pymysql.cursors.DictCursor)

#4. CRUD 쿼리문 작성 및 실행
# 1) C: CREATE, INSERT 
sql= '''CREATE TABLE IF NOT EXISTS user(
        no INT AUTO_INCREMENT PRIMARY KEY, 
        user_id VARCHAR(50) NOT NULL UNIQUE, 
        user_pw VARCHAR(255) NOT NULL, 
        email VARCHAR(100) NOT NULL UNIQUE, 
        create_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )'''
cursor.execute(sql)

# 데이터 입력
sql= '''INSERT IGNORE INTO user(user_id, user_pw, email) VALUES('aaa',SHA2('1111',256),'aa@aa.com')'''
cursor.execute(sql)

sql= '''INSERT IGNORE INTO user(user_id, user_pw, email) VALUES('bbb',SHA2('2222',256),'bb@bb.com')'''
cursor.execute(sql)

# 2) R : SELECT
sql= 'SELECT * FROM user'
cursor.execute(sql)
rows= cursor.fetchall()
for row in rows:
    print(row)  # dictionary
print()

sql= 'SELECT user_id, email FROM user'
cursor.execute(sql)
row= cursor.fetchall()
for row in rows:
    print(row)
print()

# 로그인 요청(사용자로부터 아이디와 비밀번호를 받아서 user 테이블에 해당 데이터가 있는지 검색)
user_id= 'aaa'
user_pw= '1111'

# WHERE 절에서 아이디와 비밀번호에 해당하는 데이터 검색
sql= '''
SELECT no, user_id, email
FROM user
WHERE user_id=%s AND user_pw=SHA2(%s, 256)
'''
cursor.execute(sql, (user_id, user_pw))
row= cursor.fetchone()

if row:
    print('로그인 성공!')
else:
    print('로그인 실패..')

# 3) U : UPDATE
user_id= 'aaa'
email_new= 'aa@gmail.com'
sql= '''UPDATE user SET email=%s WHERE user_id=%s'''
cursor.execute(sql, (email_new, user_id))

# 4) D : DELETE
user_id= 'bbb'
user_pw= '2222'

sql= '''DELETE FROM user WHERE user_id=%s AND user_pw=SHA2(%s,256)'''
cursor.execute(sql, (user_id, user_pw))

# 위 실핼요청이 정상적으로 적용되었는지.. 적용된 행(레코드)의 개수로 확인 가능
if cursor.rowcount == 1:
    print('삭제 성공!')
else:
    print('사용자 없음')


#----------------------------------------------------------------------------------------------------------------------------------------------------

#5. (INSER, UPDATE, DELETE)인 경우 - DB 트랜잭션 작업을 완료하도록..
db.commit()

#6. DBMS와의 연결 종료
db.close()

