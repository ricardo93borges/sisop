import threading
import time
from MemoryPosition import MemoryPosition

class Cpu(threading.Thread):

    def __init__(self, memory, consoleRequests, pcb=None, ecpu=None):
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
        self.emptyIndex = 50
        self.ecpu = ecpu
                
    def run(self):
        while True:
            #Check if CPU is blocked
            if self.blocked == True:
                time.sleep(1)
                continue
            #Get next instruction
            instruction = self.memory[self.translate(self.pc)]
            
            #Lock state
            self.lock.acquire()
            opcode = int(instruction.opcode)
            #if instruction is stop
            if opcode == 12:
                self.execInstruction(int(instruction.opcode))#Exec instruction
            else:
                self.execInstruction(int(instruction.opcode), int(instruction.opr))#Exec instruction
            self.lock.release()

    #Reset CPU state
    def reset(self):
        self.acc = self.pcb.acc
        self.pc = self.pcb.pc
        self.r0 = self.pcb.r0
        self.r1 = self.pcb.r1
        self.emptyIndex = 50

    #Save CPU state in current running program PCB
    def updateCurrentPCb(self):
        self.pcb.acc = self.acc
        self.pcb.pc = self.pc
        return self.pcb
        
    def incrementPC(self):
        self.pc += 1

    def setPC(self, position):
        self.pc = position

    #translate logical position to physical position
    def translate(self, logicalPosition):
        physicalPosition = self.r0+logicalPosition
        if self.validatePosition(physicalPosition):
            return physicalPosition
        else:
            print "Improper access"
            self.blocked = True

    #Validate if position is inside program's partition
    def validatePosition(self, position):
        if self.r0 <= position and self.r1 >= position:
            return True
        else:
            print position, self.r0, self.r1
            return False

    #Execute instruction accordingly to its opcode
    def execInstruction(self, opcode, opr=None):
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
            if self.acc > 0:
                self.setPC(int(opr))
            else:
                self.incrementPC()
        elif opcode == 8:#BRNEG
            if self.acc < 0:
                self.setPC(int(opr))
            else:
                self.incrementPC()
        elif opcode == 9:#BREQ
            if self.acc == 0:
                self.setPC(int(opr))
            else:
                self.incrementPC()
        elif opcode == 10:#IN
            self.input(self.translate(opr))
            self.incrementPC()
        elif opcode == 11:#OUT
            self.output(self.memory[self.translate(opr)].opr)
            self.incrementPC()
        elif opcode == 12:#STOP
            self.endProgram()
        elif opcode == 13:#DAT
            mp = MemoryPosition(13, int(opr))
            index = self.r0 + self.emptyIndex
            if self.r0 <= index and self.r1 >= index:
                self.memory[index] = mp
                self.emptyIndex += 1
            else:
                print 'Invalid position: ', index
                
            self.incrementPC()
        else:
            print "opcode ", opcode, " invalid"

    #Insert a input request in Console queue
    def input(self, memPos):
        self.blocked = True
        s = '%s_in_%s' %(self.pcb.pid, memPos)
        self.consoleRequests.put(s)
    
    #Insert a output request in Console queue
    def output(self, msg):
        self.blocked = True
        s = '%s_out_%s' %(self.pcb.pid, msg)
        self.consoleRequests.put(s)

    #Finish program: block CPU and remove program from memory
    def endProgram(self):
        print 'program ', self.pcb.pid,' finished'
        self.blocked = True
        self.ecpu.finishProgram(self.pcb, self.r0)        
