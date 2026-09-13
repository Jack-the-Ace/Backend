import pymysql

db= pymysql.connect(host='127.0.0.1', user='jack', password='1234', database='mbca', charset='utf8mb4')

cursor= db.cursor(pymysql.cursors.DictCursor)

sql= '''create table if not exists user(
        no int auto_increment primary key,
        user_id varchar(50) not null unique,
        user_pw varchar(255) not null,
        email varchar(100) not null unique,
        create_at TIMEstamp default current_timestamp        
        )'''
cursor.execute(sql)

sql= '''insert ignore into user(user_id, user_pw, email) Values('aaa', SHA2('1111',256), 'aa@aa.com')'''
cursor.execute(sql)
sql= '''insert ignore into user(user_id, user_pw, email) Values('bbb', SHA2('2222',256), 'bb@bb.com')'''
cursor.execute(sql)

sql= 'SELECT * FROM user'
cursor.execute(sql)
rows= cursor.fetchall()
for row in rows:
    print(row)
print()

sql='select user_id, email from user'
cursor.execute(sql)
row= cursor.fetchall()
for r in row:
    print(r)
print('=================')

user_id= 'aaa'; user_pw= '1111'

sql='''
select no, user_id, email
from user
where user_id=%s AND  user_pw=SHA2(%s, 256)
'''
cursor.execute(sql, (user_id, user_pw))
row= cursor.fetchone()

if row:
    print('로그인 성공!')
else:
    print('로그인 실패..')

user_id= 'aaa'
email_new= 'aa@gmail.com'
sql='''update user set email=%s where user_id=%s'''
cursor.execute(sql, (email_new, user_id))

user_id, user_pw= 'bbb', '2222'

sql= '''delete from user where user_id=%s And user_pw=SHA2(%s,256)'''
cursor.execute(sql, (user_id, user_pw))

if cursor.rowcount==1:
    print('삭제성공!')
else:
    print('사용자 없음')

#--------------------------------------------------------------------------------------------------------------------
db.commit()
db.close()