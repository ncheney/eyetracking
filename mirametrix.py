#! /usr/bin/env python

from __future__ import with_statement

import sys, signal
from socket import *
from time import sleep
from threading import Thread, Lock, Condition, Semaphore

from helper import getLocalIP



class Pipe(object):
    '''Pipe that carries strings.'''

    class EOF(object):
        pass

    def __init__(self, pipeSize = 100):
        self.mutex    = Semaphore(1)         # mutex for internal state
        self.contents = []                   # pipe buffer
        self.closed   = False                # whether or not the pipe is closed
        self.notFull  = Semaphore(pipeSize)  # If this is acquired, it means the pipe is not full
        self.notEmpty = Semaphore(0)         # If this is acquired, it means the pipe is not empty

    def write(self, item):
        '''Blocking write'''
        if self.closed:
            raise Exception('Write to a pipe that was already closed')

        if not isinstance(item, basestring):
            raise Exception('Can only write strings to a pipe, not %s' % repr(item))

        self.notFull.acquire()
        self.mutex.acquire()
        self.contents.append(item)
        self.mutex.release()
        self.notEmpty.release()

    def read(self):
        '''Blocking read'''
        self.notEmpty.acquire()
        self.mutex.acquire()
        item = self.contents.pop(0)
        if isinstance(item, self.EOF):
            # put the EOF character back on the pipe for other read threads to find
            self.contents.append(item)
            self.notFull.release()
            ret = None
        else:
            ret = item   # return string
        self.mutex.release()
        self.notFull.release()
        return ret

    def close(self):
        '''Close a pipe, after which:
         - writes are errors
         - reads succeed until the pipe is empty, at which point the pipe returns None (maybe like EOF??)
         Internally, this is accomplished by enlarging the pipe size by 1 and adding the EOF character to the pipe.'''
        self.mutex.acquire()
        self.closed = True
        self.contents.append(self.EOF())
        self.notEmpty.release()  # we added a character, so release an extra time
        self.mutex.release()



class Mirametrix(Thread):
    class Writer(Thread):
        '''Writer that reads from pipe and writes to mira'''
        
        def __init__(self, pipe, mira):
            Thread.__init__(self)
            self.pipe = pipe
            self.mira = mira
            self.start()

        def run(self):
            while True:
                string = self.pipe.read()
                if string is None:
                    break # pipe was closed
                print 'mira.sendall -> %s' % string
                self.mira.sendall(string)
            print 'Writer done.'                


    def __init__(self, host = 'self', port = 4242):
        Thread.__init__(self)

        if host == 'self':
            host = getLocalIP()

        self.host = host
        self.port = port
        self.addr = (self.host, self.port)
        
        self.bufferSize = 1024

        print 'Attempting to connect to %s...' % repr(self.addr),
        sys.stdout.flush()
        self.mira = socket(AF_INET, SOCK_STREAM)
        self.mira.connect(self.addr)
        print 'connected!'

        self.miraIn = Pipe(100)
        self.miraWriter = Mirametrix.Writer(self.miraIn, self.mira)

        self.lock = Lock()
        self.miraUpdate = Condition(self.lock)

        # Reader thread
        self._quit = False
        self.start()
        

        # mira state
        self._calibrateStart = None
        
    def run(self):
        self.mira.settimeout(1)
        while not self._quit:
            try:
                data = self.mira.recv(1024)
            except timeout:
                print '.',
                sys.stdout.flush()
                continue
            decoded = bytes.decode(data)
            print 'got something', decoded
            self.parse(decoded)
            #print 'running...'
            #sleep(1)

    def parse(self, string):
        print string
        RE_STRING = '<REC FPOGX="([-0-9\.]+)" FPOGY="([-0-9\.]+)" FPOGS="[0-9\.]+" FPOGD="[0-9\.]+" FPOGID="[0-9]+" FPOGV="([01])"/>'
        results = re.search(RE_STRING, st)

        if results is None:
            print 'Could not parse "%s", skipping' % st
            continue
        #print 'results is', results

        xx       = float(results.group(1))
        yy       = float(results.group(2))
        validEye = int(results.group(3))

    def getCalibrateStart(self):
        with self.lock:
            while self._calibrateStart is None:
                self.miraWrite('<GET ID="CALIBRATE_START" />')
                print 'wrote'
                self.miraUpdate.wait()
            return self._calibrateStart

    def setCalibrateStart(self, value):
        if not isinstance(value, basestring):
            value = repr(value)
        self.miraWrite('<SET ID="CALIBRATE_START" STATE="%s" />' % value)
    calibrateStart = property(getCalibrateStart, setCalibrateStart)

    def miraWrite(self, value):
        self.miraIn.write(str.encode('%s\r\n"' % value))

    def close(self):
        self._quit = True
        self.mira.close()
        print 'joining....'
        self.join()
        print 'joined, done!'

    def DEP(self):

        # Eye-tracker API specific
        tcpCliSock.sendall(str.encode('<SET ID="CALIBRATE_SHOW" STATE="0" />\r\n"'))
        sleep(1)
        tcpCliSock.sendall(str.encode('<SET ID="CALIBRATE_SHOW" STATE="1" />\r\n"'))
        sleep(1)
        tcpCliSock.sendall(str.encode('<SET ID="CALIBRATE_START" STATE="1" />\r\n"'))


        #tcpCliSock.sendall(str.encode('\r\n"'))
        #tcpCliSock.sendall(str.encode('\r\n"'))
        #
        #import pdb; pdb.set_trace()
        #tcpCliSock.sendall(str.encode('<SET ID="ENABLE_SEND_POG_FIX" STATE="1" />\r\n"'))
        #tcpCliSock.sendall(str.encode('<SET ID="ENABLE_SEND_DATA" STATE="1" />\r\n"'))

        # Loop forever
        while True:
            data = tcpCliSock.recv(1024)
            foo = bytes.decode(data)
            print 'got something', foo

        tcpCliSock.close()



def signal_handler(signal, frame, toclose):
    print 'Exiting...'
    toclose.close()
    sys.exit(0)



def main():
    host = sys.argv[1] if len(sys.argv) > 1 else 'self'
    mira = Mirametrix(host)

    signal.signal(signal.SIGINT, lambda aa, bb : signal_handler(aa, bb, mira))
    print 'Press Ctrl+C to exit'
    #signal.pause()  # [JBY] not sure why this is needed

    for ii in range(10):
        print 'calibrateStart is', mira.calibrateStart
        sleep(1)
    mira.close()



if __name__ == '__main__':
    main()

