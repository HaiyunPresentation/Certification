from ult.ClientAct import *
import sys
import time
if __name__ == "__main__":
	if(len(sys.argv)!=2):
		print("Parameter error")
		sys.exit(-1)
	
	Req = sys.argv[1].upper()
	if(Req == "PURC"):
		purchaseLicense()
		exit(0)

	beTicket = False
	if(Req == "STAR"):
		beTicket = requestTicket()

	if beTicket:
		print('now start Working...')
		print('--------------------')
		work()
		print('--------------------')
		print('Work Done, now release License...')
	else:
		print('Could not get ticket')
		exit(0)

	time.sleep(10)
	if releaseTicket():
		print('released ticket, now exit.')
	else:
		print('not released ticket, now exit.')
	exit()