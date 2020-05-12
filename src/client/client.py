from socket import *


if __name__ == "__main__":
	sock = socket(AF_INET, SOCK_DGRAM)

	sock.connect(('127.0.0.1', 10000))

	try:
		sock.send('HELO'.encode())
		info=sock.recv(1024)
		print(info.decode())
	except ConnectionError as info:
		print('连接错误！',info)
	sock.close()
