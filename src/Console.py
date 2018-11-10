import time
import threading
from MemoryPosition import MemoryPosition

class Console(threading.Thread):

    def __init__(self, memory, consoleRequests):
        threading.Thread.__init__(self, group=None, target=None, name='CONSOLE',verbose=None)
        self.lock = threading.Lock()
        self.consoleRequests = consoleRequests
        self.memory = memory

    def run(self):
        print "Thread", self.getName()

        while True:
            #check if there are console requests            
            self.lock.acquire()
            print 'Console', self.consoleRequests.qsize()
            while not self.consoleRequests.empty():
                request = self.consoleRequests.get()
                arr = request.split('_')
                print arr

                pid = arr[0]
                rtype = arr[1]
                msg = arr[2] if rtype == 'out' else None
                memPos = int(arr[2]) if rtype == 'in' else None

                if rtype == 'in':
                    i = raw_input('PID '+pid+'- > ')
                    self.memory[memPos] = MemoryPosition(13, i)
                else:
                    print 'PID', pid,'-', msg
            
            #self.consoleRequests = []
            self.lock.release()
            time.sleep(1)