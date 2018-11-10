import threading
import time

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
        self.blocked = False
                
    def run(self):
        print "Thread", self.getName()
        while True:
            if self.blocked == False:
                continue

            instruction = self.memory[self.r0+self.pc]
            self.lock.acquire()
            self.execInstruction(instruction.opcode, instruction.opr)
            self.lock.release()

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

    def execInstruction(self, opcode, opr):
        if opcode == 1: #ADD            
            self.acc += self.memory[self.translate(opr)]
            self.incrementPC()            
        elif opcode == 2:#SUB
            self.acc -= self.memory[self.translate(opr)]
            self.incrementPC()
        elif opcode == 3:#MUL
            self.acc *= self.memory[self.translate(opr)]
            self.incrementPC()
        elif opcode == 4:#DIV
            self.acc /= self.memory[self.translate(opr)]
            self.incrementPC()
        elif opcode == 5:#LOAD
            self.acc = self.memory[self.translate(opr)]
            self.incrementPC()
        elif opcode == 6:#STORE
            self.memory[self.translate(opr)] = self.acc
            self.incrementPC()
        elif opcode == 7:#BRPOS
            if self.acc > 0:
                self.setPC(opr)
        elif opcode == 8:#BRNEG
            if self.acc < 0:
                self.setPC(opr)
        elif opcode == 9:#BREQ
            if self.acc == 0:
                self.setPC(opr)
        elif opcode == 10:#IN
            self.input(self.memory[self.translate(opr)])
            self.incrementPC()
        elif opcode == 11:#OUT
            self.output(self.memory[self.translate(opr)])
            self.incrementPC()
        elif opcode == 12:#STOP
            pass
        elif opcode == 13:#DAT
            pass
        else:
            print "opcode ", opcode, " invalid"


    def input(self, memyPos):
        self.consoleRequests.append(self.pcb.pid+"_in_"+memyPos)
    
    def output(self, msg):
        self.consoleRequests.append(self.pcb.pid+"_out_"+msg)
