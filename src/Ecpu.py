import time
import threading
from Cpu import Cpu

class Ecpu(threading.Thread):

    def __init__(self, memory, consoleRequests, readyProcesses, pcbs):
        threading.Thread.__init__(self, group=None, target=None, name='ECPU',verbose=None)
        self.lock = threading.Lock()
        self.memory = memory
        self.consoleRequests = consoleRequests
        self.readyProcesses = readyProcesses
        self.pcbs = pcbs

    def run(self):
        print "Thread", self.getName()

        self.cpu = Cpu(self.memory, self.consoleRequests)
        self.cpu.start()

        while True:
            nextProcess = self.getNextProcess()
            if nextProcess != None:
                print 'exec ', nextProcess.pid
                self.cpu.pcb = nextProcess
                self.cpu.reset()
                self.cpu.blocked = False

            time.sleep(10)
        

    def getNextProcess(self):
        if self.readyProcesses.empty():
            return None
            
        #get a ready process pid
        pid = self.readyProcesses.get()        
        return self.getProcessByPid(pid)

    def getProcessByPid(self, pid):
        for pcb in self.pcbs:
            if pcb.pid == pid:
                return pcb
        return None

    def blockCpu(self):
        print 'blocking cpu'
        self.cpu.blocked = True
    
    def unblockCpu(self):
        print 'unblocking cpu'
        self.cpu.blocked = False
        
        