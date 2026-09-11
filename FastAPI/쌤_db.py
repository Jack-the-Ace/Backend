#DBMS 와 연결하는 기능을 수행하는 함수 모듈
import pymysql

def get_connection():    
    return pymysql.connect(
        host='localhost',
        user='oops',
        password='1234',
        database='mbca',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor #쿼리의 결과를 dictionary로 주도록
    )