from ult.ServerAct import *
from socket import *

if __name__ == "__main__":
	sock = socket(AF_INET, SOCK_DGRAM)
	sock.bind(('0.0.0.0', 10000))
	initDB()
	reclaimThread=ReclaimThread()
	reclaimThread.start()
	try:
		while True:			
			print('Wait for next request...')
			info, addr = sock.recvfrom(MSGLEN)
			handleRequest(sock, info, addr)

	except OSError as err:
		print('OSError!', err)
	except KeyboardInterrupt:
		stop_thread(reclaimThread)

	sock.close()
