import time
import threading
from MemoryPosition import MemoryPosition

class Console(threading.Thread):

    def __init__(self, memory, consoleRequests, ecpu):
        threading.Thread.__init__(self, group=None, target=None, name='CONSOLE',verbose=None)
        self.lock = threading.Lock()
        self.consoleRequests = consoleRequests
        self.memory = memory
        self.ecpu = ecpu

    def run(self):
        print "Thread", self.getName()

        while True:
            #check if there are any console requests
            #lock state
            self.lock.acquire()            
            while not self.consoleRequests.empty():                
                request = self.consoleRequests.get()
                arr = request.split('_')

                pid = arr[0]
                rtype = arr[1]
                msg = arr[2] if rtype == 'out' else None
                memPos = int(arr[2]) if rtype == 'in' else None

                #INPUT
                if rtype == 'in':
                    i = raw_input('PID '+pid+'- > ')
                    self.memory[memPos] = MemoryPosition(13, i)
                #OUTPUT
                else:
                    print 'PID', pid,'-', msg

                self.unblockCpu()
            
            #unlock state
            self.lock.release()
            time.sleep(1)

    def blockCpu(self):
        self.ecpu.blockCpu()
    
    def unblockCpu(self):
        self.ecpu.unblockCpu()