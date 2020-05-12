import re
from socket import *

MSGLEN = 128


def handle_request(sock, info, addr):
	if(re.match(r'HELO.*', info.decode())):
		sock.sendto('WELC'.encode(), addr)
	#print(info.decode())
	return


if __name__ == "__main__":
	sock = socket(AF_INET, SOCK_DGRAM)

	sock.bind(('0.0.0.0', 10000))

	ticket_array = []

	TICKET_AVAIL = 0

	distributed_tickets = 0

	MAXUSERS = 1024

	try:
		while True:
			print('等待连接...')

			info, addr = sock.recvfrom(MSGLEN)
			print('...收到：',info,'连接自：',addr)
			handle_request(sock,info,addr)
	except OSError as info:
		print('OSError!', info)

	sock.close()
