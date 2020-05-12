from ult.ClientAct import *

if __name__ == "__main__":
	if showTicket:
		beTicket, ticket = requestTicket(KeyFormat)
	else:
		beTicket = requestTicket(KeyFormat)

	if beTicket:
		print('now start Working...')
		print('--------------------')
		work()
		print('--------------------')
		print('Work Done, now release License...')
	else:
		print('Could not get ticket')
		exit(0)

	if releaseTicket(ticket):
		print('released ticket, now exit.')
	else:
		print('not released ticket, now exit.')
	exit()