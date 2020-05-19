from ult.config import *
from socket import *
from random import randint
import re
import cx_Oracle
import sqlite3
import time
import threading
import schedule
import inspect
import ctypes

Tickets = {}
madeTickets = False


def _async_raise(tid, exctype):
	"""raises the exception, performs cleanup if needed"""
	tid = ctypes.c_long(tid)
	if not inspect.isclass(exctype):
		exctype = type(exctype)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, ctypes.py_object(exctype))
	if res == 0:
		raise ValueError("invalid thread id")
	elif res != 1:
		# """if it returns a number greater than one, you're in trouble,
		# and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		raise SystemError("PyThreadState_SetAsyncExc failed")
 
 
def stop_thread(thread):
	_async_raise(thread.ident, SystemExit)

class ReclaimThread(threading.Thread):
	def run(self):
		schedule.every(5).seconds.do(checkReclaim)
		while True:
			schedule.run_pending()


# 制作一份随机票据, 票据长度由'utl.config' 中决定
def makeTicke():
	ticket = ''
	for i in range(0, lenTicket):
		ticket += str(randint(0, 9))

	return ticket


def makeLicense():
	license = ''
	for i in range(0, lenLicense):
		license += str(randint(0, 9))

	return license


# 定期检查客户端是否向
def checkReclaim():
	print('>Checked reclaim info:')
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	sql = "select * from client"
	curs.execute(sql)
	res = curs.fetchall()
	#print(res)
	for line in res:
		latestTime=time.strptime(line[1],'%Y/%m/%d %H:%M:%S')
		if time.time()-time.mktime(latestTime)>30:
			print('delete: Tno=',line[0],' latestTime=',line[1],', lno=',line[2])
			sql = "delete from client where Tno={} and latestTime='{}'".format(line[0],line[1])
			curs.execute(sql)
			conn.commit()
	return


# 获取当前使用人数
def getUserNum(license):
	#conn = cx_Oracle.connect('test', 'test', 'localhost:1521/XE')
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	sql = "select count(*) from client where lno = {}".format(license)
	curs.execute(sql)
	userNum = curs.fetchall()[0][0]
	curs.close()
	conn.close()
	return userNum


# 获取许可证最多使用人数
def getMaxNum(license):
	#conn = cx_Oracle.connect('test', 'test', 'localhost:1521/XE')
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	sql = "select userNum from license where lno = {}".format(license)
	curs.execute(sql)
	res = curs.fetchall()
	print(res, 'len=', len(res))
	if len(res) == 0:
		return -1
	maxNum = res[0][0]
	print('maxNum=', maxNum)
	curs.close()
	conn.close()
	return maxNum


# 查询票据
def searchTicket(ticket, license):
	#conn = cx_Oracle.connect('test', 'test', 'localhost:1521/XE')
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	exist = 0
	sql = "select count(*) from client where Tno = '{0}' and Lno = '{1}'".format(
		ticket, license)
	try:
		curs.execute(sql)
		exist = curs.fetchall()[0][0]
	except cx_Oracle.DatabaseError as msg:
		print(msg)
	except cx_Oracle.InterfaceError as msg:
		print(msg)
	if exist == 1:
		return True
	return False


# 申请票据, 若票据被完全占用则返回空
def requestTicket(license):
	userNum = getUserNum(license)

	maxNum = getMaxNum(license)

	#当前人数小于许可证所允许人数则颁发票据
	if (userNum < maxNum):
		#conn = cx_Oracle.connect('test', 'test', 'localhost:1521/XE')
		conn = sqlite3.connect('info.db')
		curs = conn.cursor()
		sql = 'insert into client(Tno,latestTime,Lno) values (:Tno,:latestTime,:Lno)'
		param = []
		ticke = makeTicke()
		param.append(ticke)
		param.append(
			time.strftime('%Y/%m/%d %H:%M:%S', time.localtime(time.time())))
		param.append(license)
		try:
			curs.execute(sql, param)

		except cx_Oracle.DatabaseError as msg:
			print(msg)
			#返回失败
			return ""

		conn.commit()
		curs.close()
		conn.close()
		return ticke

	return ''


# 票据归还，暂无
def updateTicket(Req):
	return


# 归还票据操作
def releaseTicket(ticket, license):
	#conn = cx_Oracle.connect('test', 'test', 'localhost:1521/XE')
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	sql = "delete from client where lno = {} and Tno = {}".format(
		license, ticket)
	try:
		curs.execute(sql)
		conn.commit()
	except cx_Oracle.DatabaseError as msg:
		print(msg)
		return False
	return True


# 服务器处理用户票据申请
def doHELO(info):
	req = re.findall('\d{10}', info)
	sendM = ''

	if req == []:
		# 无法认证
		print('>Requst Unknown')
		sendM = 'RFUS:Could not recognize your reqest'
	else:
		license = req[0]

		# 伪造的证书
		if checkLicense(license) == False:
			print('>License error...')
			sendM = 'RFUS:License error'
			return sendM

		ticket = requestTicket(license)
		if ticket:
			print(
				'>Deliver ticket:', ticket,
				'(rest:' + str(getMaxNum(license) - getUserNum(license)) + ')')
			sendM = 'WELC:' + ticket
		else:
			# 票据已被最多次申请
			print('>NO ticket chance remain...')
			sendM = 'RFUS:No ticket rest'

	return sendM


def doCKAL(info):
	rels = re.findall('\d{20}', info)
	sendM = ''

	if rels == []:
		# 无法认证
		print('>Requst Unknown')
		sendM = 'UKNW:Cannot recognize your request'
	else:
		license = rels[0][0:10]
		ticket = rels[0][10:]
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	latestTime = time.strftime('%Y/%m/%d %H:%M:%S',
							   time.localtime(time.time()))
	sql = "update client set latesttime='{}' where lno = {} and Tno = {}".format(
		latestTime, license, ticket)
	try:
		curs.execute(sql)
		conn.commit()
	except error:
		return 'FAIL: Failed to updatw'
	sendM = 'GOOD:'
	return sendM


# 检查许可证
def checkLicense(license):
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	sql = "select count(*) from license where lno = {}".format(license)
	curs.execute(sql)
	result = curs.fetchall()[0][0]
	conn.close()
	if result == 1:
		return True
	return False


# 服务器处理用户票据归还
def doRELS(info):
	rels = re.findall('\d{20}', info)
	sendM = ''

	if rels == []:
		# 无法认证
		print('>Requst Unknown')
		sendM = 'UKNW:Cannot recognize your request'
	else:
		license = rels[0][0:10]
		ticket = rels[0][10:]

		if searchTicket(ticket, license) == False:
			# 试图归还一个和许可证不匹配的票据
			print('>>WARNING<< someone try to release an unused ticket!!')
			sendM = 'WARN:!!!'

		elif searchTicket(ticket, license) == True:
			# 许可证和票据配对, 正常归还
			releaseTicket(ticket, license)
			print(">Release ticket")
			sendM = 'GBYE:Thank you for your using'

	return sendM


# 服务器处理收到的购买许可证请求并作出答复
def doPURC(info):
	license = makeLicense()
	infos = info.split(':')
	userName = infos[1]
	password = infos[2]
	userNum = int(infos[3])
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	#sql语句
	sql = 'insert into license(Lno,userName,password,userNum) values (:license,:userName,:password,:userNum)'
	param = []
	param.append(license)
	param.append(userName)
	param.append(password)
	param.append(userNum)
	try:
		curs.execute(sql, param)
	except cx_Oracle.DatabaseError as msg:
		print(msg)
		sendM = "FAIL:Insert error"
		#返回失败
		return sendM
	print("License generated successfully")
	sendM = "PERM:" + license
	conn.commit()
	return sendM


# 服务器处理收到的请求并做出答复
def handleRequest(sock, info, addr):
	info = info.decode()
	check = info[:4]
	sendM = ''

	# 处理请求
	if check == 'HELO':
		# 用户请求票据
		print('-Request Ticket with License:', info, 'from: ', addr)
		sendM = doHELO(info)

	elif check == 'CKAL':
		# 用户报告活动状态
		print('-Request for checking', info, 'from: ', addr)
		sendM = doCKAL(info)

	elif check == 'RELS':
		# 用户归还票据
		print('-Request for releasing:', info, 'from: ', addr)
		sendM = doRELS(info)

	elif check == 'PURC':
		print("Generate license...")
		sendM = doPURC(info)
	else:
		# 无法识别信息
		print('-Request Unrecognized:', info, 'from: ', addr)
		sendM = 'UKNW:???'

	# 答复
	sock.sendto(sendM.encode(), addr)
	return


# 初始化SQLite数据库
def initDB():
	conn = sqlite3.connect('info.db')
	curs = conn.cursor()
	try:
		sql = "select * from license"
		curs.execute(sql)
		print('Table LICENSE has been created')
	#没有license表时应先创建
	except sqlite3.OperationalError:
		sql = "create table license(Lno char(10),userName char(20),password char(20),userNum int)"
		print('Create table license...')
		curs.execute(sql)

	try:
		sql = "select * from client"
		curs.execute(sql)
		print('Table CLIENT has been created')

	#没有client表时应先创建
	except sqlite3.OperationalError:
		sql = "create table client(Tno char(20),latestTime char(20),Lno char(20))"
		print('Create table CLIENT...')
		curs.execute(sql)

	conn.commit()
	return
