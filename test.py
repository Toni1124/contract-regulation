import psycopg2

conn = psycopg2.connect(host = '10.0.2.251', dbname = 'db', user = 'ethereum', password = 'emm20240809!')
#conn = psycopg2.connect(host = '162.105.88.203', dbname = 'db', user = 'ethereum', password = 'emm20240809!')

cursor = conn.cursor()

cursor.execute('create table test(a int)')

cursor.execute('insert into test values(1)')
cursor.execute('insert into test values(2)')
cursor.execute('insert into test values(3)')

#conn.commit() #ddl和dml的结果需要提交事务才能被持久化

cursor.execute('select * from test')
res = cursor.fetchall()


print(res)