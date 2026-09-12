import pymysql
db= pymysql.connect(
    host='127.0.0.1', port=3306, user='jack', 
    passwd='1234', database='mbca', charset='utf8mb4'
)
cursor=db.cursor()
cursor=db.cursor(pymysql.cursors.DictCursor)

sql= 'SELECT * FROM BOOK'
cursor.execute(sql)

rows= cursor.fetchall()
print(rows)
print('-----------------all------------')
#----------------------------------
sql= 'select*from book'
cursor.execute(sql)

row= cursor.fetchone()
print(row)
print(cursor.fetchone())
print(cursor.fetchone())
print(cursor.fetchone())
print('------------------one------------')

rows= cursor.fetchmany(3)
print(rows)
print(cursor.fetchmany(3))
print('------------------many------------')
#--------------------------------------------
sql= 'select*from book where boOk_iD=4'
cursor.execute(sql)
row= cursor.fetchone()
print(row)
print(cursor.fetchone())
print(row)
print(cursor.fetchone())

db.commit()

db.close()

