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
        self.index = 0

    def run(self):
        print "Thread", self.getName()

        cpu = Cpu(self.memory, self.consoleRequests)
        cpu.start()

        while True:
            nextProcess = self.getNextProcess()
            if nextProcess != None:
                print 'exec ', nextProcess.pid
                cpu.pcb = nextProcess
                cpu.reset()
                cpu.blocked = False

            time.sleep(10)
        

    def getNextProcess(self):
        if len(self.readyProcesses) == 0:
            return None
        
        if self.index >= len(self.readyProcesses):
            self.index = 0
        
        #get a ready process pid
        pid = self.readyProcesses[self.index]
        
        #remove process
        del self.readyProcesses[self.index]

        self.index += 1
        return self.getProcessByPid(pid)

    def getProcessByPid(self, pid):
        for pcb in self.pcbs:
            if pcb.pid == pid:
                return pcb
        return None
        
        