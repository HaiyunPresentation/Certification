from ult.ClientAct import *
from ult.killThread import *
import sys
import time
import schedule

def usage():
    print('License Client by HaiyunPresentation')
    print('Usage: ')
    print('    python client.py [--mode]')
    print('Mode list:')
    print('  -p, --purchse')
    print('  -r, --run')
    print('\'python3\' is recommended in Linux')


if __name__ == "__main__":
    if (len(sys.argv) != 2):
        print("Parameter error")
        usage()
        sys.exit(-1)

    Req = sys.argv[1]
    if (Req == '-p' or Req == '--purchase'):
        try:
            purchaseLicense()
        except KeyboardInterrupt:
            print('KeyboardInterrupt...')
            pass
        exit(0)

    err = ''
    if (Req == '-r' or Req=='--run'):
        err = requestTicket()
    else: # 指令错误
        usage()
        sys.exit(-1)

    if err != '':
        print('Could not get ticket: ', err)
        exit(0)
    try:
        checkAliveThread=CheckAliveThread()
        checkAliveThread.start()
        print('Now start working...')
        print('--------------------')
        work()
        print('--------------------')
        print('Done, now release the license...')
    except KeyboardInterrupt:
        print('KeyboardInterrupt...')
        pass
        
    if releaseTicket():
        print('Released ticket, now exit.')
    else:
        print('Cannot released ticket, now exit.')
    stop_thread(checkAliveThread)
    exit(0)
