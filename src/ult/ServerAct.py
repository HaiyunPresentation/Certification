from ult.config import *
from socket import *
from random import randint
import re

Tickets = {}
TStatus = {}
madeTickets = False

# 制作一份随机票据, 票据长度由'utl.config' 中决定
def makeTicke():
	ticket = ''
	for i in range(0, lenTicket):
		ticket += str(randint(0, 9))

	return ticket


# 该函数仅允许调用一次, 制作所有票据与票据状态记录
# 票据数量由'utl.config'  中决定
# 一次创建, 后续不允许添加, 仅允许更新
def makeTickets():
	global madeTickets
	if not madeTickets:
		# 为每组请求制定票据
		for i in range(1, nTicket+1):
			tno = str(i)
			if len(tno) == 1:
				tno = '0'+tno

			Tickets['xmu-network-t'+tno] = makeTicke()
			# TStatus['xmu-network-t'+tno] = [False, False]
			# 计划一: 分别为C/S 端的票据占用情况
			TStatus['xmu-network-t'+tno] = 0
			# 计划二: 记录同一票据申请情况, 应不超过2
		
		madeTickets = True
	else:
		return False

	return True


# 申请票据, 若票据被完全占用则返回空
def requestTicket(Req):
	if TStatus[Req] < 2:
		TStatus[Req] += 1
		return Tickets[Req]
	
	return ''	


# 一份票据归还后失效, 并进行更新
def updateTicket(Req):
	Tickets[Req] = makeTicke()


# 归还票据操作, 若使票据无人占用则更新
def releaseTicket(Req):
	if TStatus[Req] == 0:
		return False
	else:
		TStatus[Req] -= 1

	if TStatus[Req] == 0:
		updateTicket(Req)
	
	return True


# 服务器处理用户票据申请
def doHELO(info):
	req = re.findall('xmu-network-t\d\d', info)
	sendM = ''

	if req == []:
		# 无法认证
		print('>Requst Unknown')
		sendM = 'RFUS:Could not recognize your reqest'
	else:
		Req = req[0]

		ticket = requestTicket(Req)
		if ticket:
			print('>Deliver ticket:', ticket, '(rest:'+str(2-TStatus[Req])+')')
			sendM = 'WELC:'+ticket
		else:
			# 票据已被最多次申请
			print('>NO ticket chance remain...')
			sendM = 'RFUS:NO ticket rest'
	
	return sendM


# 服务器处理用户票据归还
def doRELS(info):
	rels  = re.findall('xmu-network-t\d\dby:\d\d\d\d\d\d\d\d\d\d', info)
	sendM = ''

	if rels == []:
		# 无法认证
		print('>Requst Unknown')
		sendM = 'UKNW:Could not recognize your reqest'
	else:
		Rels = rels[0][:15]
		ticket = rels[0][18:]

		if TStatus[Rels] == 0:
			# 试图归还一个未被授权的票据
			print('>>WARNING<< someone try to release an unused ticket!!')
			sendM = 'WARN:!!!'

		elif Tickets[Rels] == ticket:
			# 授权申请和票据配对, 正常归还
			releaseTicket(Rels)
			print(">Release ticket")
			sendM = 'GBYE:Thank you for your using'
		else:
			# 试图归还不匹配的申请和票据
			print(">>WARNING<< someone try to release an ticket by Unmatched req-ticket")
			sendM = 'WARN:Unmatched release-ticket'
	
	return sendM


# 服务器处理收到的请求并做出答复
def handle_request(sock, info, addr):
	info  = info.decode()
	check = info[:4]
	sendM = ''

	# 处理请求
	if check == 'HELO':
		# 用户请求票据
		print('-Request Ticket:', info, 'from: ', addr)
		sendM = doHELO(info)
		
	elif check == 'RELS':
		# 用户归还票据
		print('-Request Release:', info, 'from: ', addr)
		sendM = doRELS(info)
		
	else:
		# 无法识别信息
		print('-Request Unrecognized:', info, 'from: ', addr)
		sendM = 'RFUS:???'
	
	# 答复
	sock.sendto(sendM.encode(), addr)
	return

makeTickets()