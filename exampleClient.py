#! /usr/bin/env python

import sys
from socket import *

from helper import getLocalIP



def main():
    if len(sys.argv) > 1:
        HOST = sys.argv[1]
    else:
        #HOST = '128.253.224.134'
        #HOST = '128.84.62.237'
        #HOST = '10.211.55.3'
        #HOST = '192.168.0.115'
        #HOST = getLocalIP()
	HOST = '128.253.224.94'

    PORT = 4242
    BUFSIZ = 1024
    ADDR = (HOST, PORT)

    print 'Attempting to connect to %s...' % repr(ADDR),
    sys.stdout.flush()
    tcpCliSock = socket(AF_INET, SOCK_STREAM)
    tcpCliSock.connect(ADDR)
    print 'connected!'

    # Eye-tracker API specific
    tcpCliSock.send(str.encode('<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n"'))
    tcpCliSock.send(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n"'))

    # Loop forever
    while 1:
        data = tcpCliSock.recv(1024)
        foo = bytes.decode(data)
        print 'got something', foo

    tcpCliSock.close()



if __name__ == '__main__':
    main()

