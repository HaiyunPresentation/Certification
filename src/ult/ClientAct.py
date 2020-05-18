from ult.config import *
from socket import *

import re


ticket = ''

# 根据给出申请语句向服务器申请票据, 申请语句格式参见 'ult.config' 或'README'
def requestTicket(Req):
	print('Getting Ticket...')
	sock = socket(AF_INET, SOCK_DGRAM)

	reqTimes = 3
	while reqTimes:
		reqTimes -= 1
		
		try:
			msg = 'HELO:'+Req
			sock.sendto(msg.encode(), ServerIP_Port)
			info = sock.recv(MSGLEN).decode()

			check = info[:4]
			if check != 'WELC' and check != 'RFUS':
				print('Unknown message:', info)
				sock.close()
				return False
				# 收到错误信息, 立即退出
			break

		except ConnectionError as Err:
			print('Connect Error',Err)
			continue

	sock.close()

	global ticket
	ticket = info[5:]
	return info[:4]=='WELC'
	# if showTicket:
	# 	return info[:4]=='WELC', info
	# else:
	# 	ticket = info
	# 	return info[:4]=='WELC'

# 开始工作进程
def work():
	# 填入封装项目二
    pass

# 向服务器归还票据
def releaseTicket(Req):
	print('Release Ticket...')
	sock = socket(AF_INET, SOCK_DGRAM)

	relsTimes = 3
	while relsTimes:
		relsTimes -= 1

		try:
			msg = 'RELS:'+Req+' by:'+ticket
			sock.sendto(msg.encode(), ServerIP_Port)
			info = sock.recv(MSGLEN).decode()
			break
		except ConnectionError as Err:
			print('Connect Error', Err)
			print('try again... (rest times: '+str(relsTimes)+')')
			continue

	sock.close()
	return info[:4] == 'GBYE'
	# 仅严格返回是否成功向服务器提出归还
	# 即使归还失败也仍然退出
	# 由服务器超时自动收回票据
