from ult.ClientAct import *
import sys
import time
import schedule

if __name__ == "__main__":
	if (len(sys.argv) != 2):
		print("Parameter error")
		sys.exit(-1)

	Req = sys.argv[1].upper()
	if (Req == "PURC"):
		purchaseLicense()
		exit(0)

	err = ''
	if (Req == "STAR"):
		err = requestTicket()

	if err == '':
		checkAliveThread=CheckAliveThread()
		checkAliveThread.start()
		print('Now start working...')
		print('--------------------')
		work()
		print('--------------------')
		print('Done, now release the license...')
	else:
		print('Could not get ticket: ', err)
		exit(0)
		


	if releaseTicket():
		print('Released ticket, now exit.')
	else:
		print('Cannot released ticket, now exit.')
	stop_thread(checkAliveThread)
	exit(0)
