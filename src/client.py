from ult.ClientAct import *

if __name__ == "__main__":
	Req = 'foaughifoi'
	
	# 是否将ticket 封装, 由'utl.config' 决定
	# if showTicket:
		# beTicket, ticket = requestTicket(Req)
	# else:
		# beTicket = requestTicket(Req)
	beTicket = requestTicket(Req)

	if beTicket:
		print('now start Working...')
		print('--------------------')
		work()
		print('--------------------')
		print('Work Done, now release License...')
	else:
		print('Could not get ticket')
		exit(0)

	if releaseTicket(Req):
		print('released ticket, now exit.')
	else:
		print('not released ticket, now exit.')
	exit()