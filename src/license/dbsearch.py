import sqlite3


def searchAll(table):
    conn = sqlite3.connect('info.db')
    curs = conn.cursor()
    colsql = "PRAGMA table_info([" + table + "])"
    curs.execute(colsql)
    collist = curs.fetchall()
    sql = "select * from " + table
    curs.execute(sql)
    #conn.commit()
    res = curs.fetchall()
    response = '<table border="1"><tr>'
    for colinfo in collist:
        response += '<th>' + colinfo[1] + '</th>'
    response += '</tr>'
    for var in res:
        response += '<tr>'
        for col in var:
            response += '<td>' + str(col) + '</td>'
        response += '</tr>'
    return response + "</table>"