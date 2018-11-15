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
        
        # Get next ready program to run 
        # or keep running current program if there is no other program
        # Use round-robin algorithms with a quantum = 10 to schedule process  
        while True:
            # Get next ready program
            nextProcess = self.getNextProcess()
            # If there is no ready program check if there is a program in pcb list to run
            if nextProcess == None and len(self.pcbs) > 0:
                nextProcess = self.pcbs[0]

            if nextProcess != None:
                #update current process running pcb
                if self.cpu.pcb != None:
                    self.updateCurrentPcb()

                # Run next program
                print 'Running => ', nextProcess.pid, ' r0:', nextProcess.r0, ' r1:', nextProcess.r1
                #self.dumpPartition(nextProcess.r0)            
                self.cpu.pcb = nextProcess
                self.cpu.ecpu = self
                self.cpu.reset()
                self.cpu.blocked = False

            # Wait 10 seconds 
            time.sleep(10)
        
    def updateCurrentPcb(self):
        currentPcb = self.cpu.updateCurrentPCb()
        for pcb in self.pcbs:
            if pcb.pid == currentPcb.pid:
                pcb.acc = currentPcb.acc
                pcb.pc = currentPcb.pc
                break


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
        self.cpu.blocked = True
    
    def unblockCpu(self):
        self.cpu.blocked = False

    def finishProgram(self, pcb, r0):
        self.removeProgram(r0)
        self.removePcb(pcb)

    #remove a pcb from the pcb list
    def removePcb(self, pcb):
        i = 0
        while i < len(self.pcbs):
            if self.pcbs[i].pid == pcb.pid:
                del self.pcbs[i]
                break
            i += 1

    #Remove program from memory
    def removeProgram(self, r0):
        i = r0
        while i < 64:
            self.memory[i] = None
            i += 1

    #Dump what is in a partition for debug purpose 
    def dumpPartition(self, r0):
        i = r0
        while i < 64:
            if self.memory[i] == None:
                print i, ':', None
            else:    
                print i, ':', 'opcode', self.memory[i].opcode, 'opr', self.memory[i].opr
            i += 1
        
        