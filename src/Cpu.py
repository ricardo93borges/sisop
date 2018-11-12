import threading
import time
from MemoryPosition import MemoryPosition

class Cpu(threading.Thread):

    def __init__(self, memory, consoleRequests, pcb=None):
        threading.Thread.__init__(self, group=None, target=None, name='CPU',verbose=None)
        self.lock = threading.Lock()
        self.memory = memory
        self.acc = 0
        self.pc = 0
        self.r0 = 0
        self.r1 = 0
        self.pcb = pcb
        self.consoleRequests = consoleRequests
        self.blocked = True
                
    def run(self):
        while True:
            if self.blocked == True:
                time.sleep(1)
                continue

            instruction = self.memory[self.r0+self.pc]
            self.lock.acquire()

            opcode = int(instruction.opcode)
            if opcode == 12:
                self.execInstruction(int(instruction.opcode))
            else:
                self.execInstruction(int(instruction.opcode), int(instruction.opr))
            #print 'acc', self.acc
            #self.endProgram()
            self.lock.release()

    def reset(self):
        self.acc = self.pcb.acc
        self.pc = self.pcb.pc
        self.r0 = self.pcb.r0
        self.r1 = self.pcb.r1

    def incrementPC(self):
        if self.validatePosition(self.pc+1):
            self.pc += 1
        else:
            print "Improper access"

    def setPC(self, position):
        if self.validatePosition(position):
            self.pc = position
        else:
            print "Improper access"

    def translate(self, logicalPosition):
        physicalPosition = self.r0+logicalPosition
        if self.validatePosition(physicalPosition):
            return physicalPosition
        else:
            print "Improper access"

    def validatePosition(self, position):
        if self.r0 <= position and self.r1 >= position:
            return True
        else:
            return False

    def execInstruction(self, opcode, opr=None):
        #print 'opcode', opcode, 'opr', opr
        if opcode == 1: #ADD            
            self.acc += int(self.memory[self.translate(opr)].opr)
            self.incrementPC()            
        elif opcode == 2:#SUB
            self.acc -= int(self.memory[self.translate(opr)].opr)
            self.incrementPC()
        elif opcode == 3:#MUL
            self.acc *= int(self.memory[self.translate(opr)].opr)
            self.incrementPC()
        elif opcode == 4:#DIV
            self.acc /= int(self.memory[self.translate(opr)].opr)
            self.incrementPC()
        elif opcode == 5:#LOAD
            self.acc = int(self.memory[self.translate(opr)].opr)
            self.incrementPC()
        elif opcode == 6:#STORE
            mp = MemoryPosition(13, int(self.acc))
            self.memory[self.translate(opr)] = mp
            self.incrementPC()
        elif opcode == 7:#BRPOS
            print 'brpos'
            if self.acc > 0:
                self.setPC(int(opr))
        elif opcode == 8:#BRNEG
            if self.acc < 0:
                self.setPC(int(opr))
        elif opcode == 9:#BREQ
            print 'breq', self.acc, int(opr)
            if self.acc == 0:
                self.setPC(int(opr))
        elif opcode == 10:#IN
            self.input(self.translate(opr))
            self.incrementPC()
        elif opcode == 11:#OUT
            self.output(self.memory[self.translate(opr)].opr)
            self.incrementPC()
        elif opcode == 12:#STOP
            self.endProgram()
        elif opcode == 13:#DAT
            pass
        else:
            print "opcode ", opcode, " invalid"


    def input(self, memPos):
        self.blocked = True
        s = '%s_in_%s' %(self.pcb.pid, memPos)
        self.consoleRequests.put(s)
    
    def output(self, msg):
        s = '%s_out_%s' %(self.pcb.pid, msg)
        self.consoleRequests.put(s)

    #TODO remove program from memory
    def endProgram(self):
        print 'finished'
        print 'acc', self.acc
        print self.memory[20].opr
        print self.memory[21].opr
        print self.memory[22].opr
        print self.memory[23].opr
        self.blocked = True        
        """ if self.pc == self.r1 or self.memory[self.r0+self.pc] == None:
            print 'finished'
            self.blocked = True """
