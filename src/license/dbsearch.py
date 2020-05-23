import sqlite3

def deleteLicense(Lno):
    conn = sqlite3.connect('info.db')
    curs = conn.cursor()
    sql = "delete * from license where lno='"+Lno+"'"
    curs.execute(sql)
    conn.commit()
    return 'Successfully delete!'

def searchAll(table):
    conn = sqlite3.connect('info.db')
    curs = conn.cursor()
    colsql = "PRAGMA table_info([" + table + "])"
    curs.execute(colsql)
    collist = curs.fetchall()
    sql = "select * from " + table
    curs.execute(sql)
    res = curs.fetchall()
    response = '<table class="table table-striped"><tr>'
    for colinfo in collist:
        response += '<th>' + colinfo[1] + '</th>'
    response += '</tr>'
    for var in res:
        response += '<tr>'
        for col in var:
            response += '<td>' + str(col) + '</td>'
        response += '</tr>'
    return response + "</table>"