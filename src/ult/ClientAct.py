from ult.config import *
from socket import *
import os
import threading
import schedule
import time

ticket = ''
license = ''


class CheckAliveThread(threading.Thread):
	def run(self):
		schedule.every(5).seconds.do(checkAlive)
		while True:
			schedule.run_pending()

#购买许可证
def purchaseLicense():
	sock = socket(AF_INET, SOCK_DGRAM)

	#尝试次数
	reqTimes = 3
	while reqTimes:
		reqTimes -= 1

		try:
			userName = input("Please enter user name:")
			if (userName == ""):
				print("Username can not be empty")
				continue
			password = input("Please enter the password:")
			if (password == ""):
				print("password can not be empty")
				continue
			userNum = input("Please enter the number of users:")
			if (userNum == ""):
				print("The number of users can not be empty")
				continue
			try:
				int(userNum)
			except Exception as ex:
				print("The number of users must be an integer")
				continue

			#使用:作为分隔符
			msg = 'PURC:' + userName + ':' + password + ':' + userNum
			sock.sendto(msg.encode(), ServerIP_Port)
			info = sock.recv(MSGLEN).decode()

			check = info[:4]

			if check == 'PERM':
				print("Successfully purchased")
				print("The license is:" + info[5:])
				sock.close()
				return True
			elif check == 'FAIL':
				print("Failed to purchase")
			else:
				print('Unknown message:', info)
				sock.close()
				return False
				# 收到错误信息, 立即退出
			break
		except ConnectionError as Err:
			print('Connection Error', Err)
			continue
	print("Purchase failed: Cannot receive from the license server!")
	sock.close()
	return False


# 根据给出申请语句向服务器申请票据, 申请语句格式参见 'ult.config' 或'README'
def requestTicket():

	#是否已通过验证
	Verified = False
	global license
	filename = "license.lic"
	if (os.path.isfile("license.lic") == True):
		Verified = True
		with open(filename, "r") as reader:
			license = reader.readline()

	else:
		license = input("Please enter a license:")

	sock = socket(AF_INET, SOCK_DGRAM)
	connected = False
	reqTimes = 3
	check = ''
	while reqTimes:
		reqTimes -= 1

		try:
			msg = 'HELO:' + license
			sock.sendto(msg.encode(), ServerIP_Port)
			info = sock.recv(MSGLEN).decode()

			check = info[:4]

			if check != 'WELC' and check != 'RFUS':
				print('Unknown message:', info)
				sock.close()
				return False
				# 收到错误信息, 立即退出
			connected = True
			break

		except ConnectionError as Err:
			print('Connection Error', Err)
			continue

	sock.close()
	if connected == False:
		return 'Failed to connect the server'

	if check == 'RFUS':
		return info[5:]

	#第一次通过验证后将许可证保存起来
	if (check == 'WELC') and Verified == False:
		with open(filename, "w") as writer:
			writer.write(license)

	global ticket
	ticket = info[5:]
	return ''

# 每隔一段时间向服务器发送请求检查许可状态
def checkAlive():
	print('\n------\nChecking alive...')
	sock = socket(AF_INET, SOCK_DGRAM)

	checkTimes = 3
	while checkTimes:
		checkTimes -= 1
		try:
			msg = 'CKAL:' + license + ticket
			print("msg :" , msg, '\n------')
			sock.sendto(msg.encode(), ServerIP_Port)
			info = sock.recv(MSGLEN).decode()
			break
		except ConnectionError as Err:
			#print('Connection Error', Err)
			print('try again... (rest times: ' + str(checkimes) + ')')
			continue

	sock.close()
	return info[:4] == 'GOOD'

# 开始工作进程
def work():
	# 填入封装项目二
	while True:
		str = ''
		str = input()
		print(str)
		if str == 'exit':
			break


# 向服务器归还票据
def releaseTicket():
	print('Releasing Ticket...')
	sock = socket(AF_INET, SOCK_DGRAM)

	relsTimes = 3
	while relsTimes:
		relsTimes -= 1

		try:
			msg = 'RELS:' + license + ticket
			print("msg :" + msg)
			sock.sendto(msg.encode(), ServerIP_Port)
			info = sock.recv(MSGLEN).decode()
			break
		except ConnectionError as Err:
			print('Connection Error', Err)
			print('try again... (rest times: ' + str(relsTimes) + ')')
			continue

	sock.close()
	return info[:4] == 'GBYE'
	# 仅严格返回是否成功向服务器提出归还
	# 即使归还失败也仍然退出
	# 由服务器超时自动收回票据
