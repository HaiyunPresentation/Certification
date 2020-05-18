import cx_Oracle

conn = cx_Oracle.connect('test', 'test', 'localhost:1521/XE')
curs = conn.cursor()
sql='SELECT * FROM t' #sql语句

rr=curs.execute (sql)

row=curs.fetchone()

print(row[0])

curs.close()

conn.close()
