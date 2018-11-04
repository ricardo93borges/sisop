import threading

class Cpu(threading.Thread):

    def __init__(self, memory):
        threading.Thread.__init__(self, group=None, target=None, name='CPU',verbose=None)
        self.lock = threading.Lock()
        self.memory = memory
        self.acc = 0
        self.pc = 0
        self.r0 = 0
        self.r1 = 0
                
    def run(self):
        print "Thread", self.getName()

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
            self.lock.acquire()
            self.acc += self.memory[self.translate(opr)]
            self.incrementPC()
            self.lock.release()
        elif opcode == 2:#SUB
            self.lock.acquire()
            self.acc -= self.memory[self.translate(opr)]
            self.incrementPC()
            self.lock.release()
        elif opcode == 3:#MUL
            self.lock.acquire()
            self.acc *= self.memory[self.translate(opr)]
            self.incrementPC()
            self.lock.release()
        elif opcode == 4:#DIV
            self.lock.acquire()
            self.acc /= self.memory[self.translate(opr)]
            self.incrementPC()
            self.lock.release()
        elif opcode == 5:#LOAD
            self.lock.acquire()
            self.acc = self.memory[self.translate(opr)]
            self.incrementPC()
            self.lock.release()
        elif opcode == 6:#STORE
            self.lock.acquire()
            self.memory[self.translate(opr)] = self.acc
            self.incrementPC()
            self.lock.release()
        elif opcode == 7:#BRPOS
            self.lock.acquire()
            if self.acc > 0:
                self.setPC(opr)
            self.lock.release()
        elif opcode == 8:#BRNEG
            self.lock.acquire()
            if self.acc < 0:
                self.setPC(opr)
            self.lock.release()
        elif opcode == 9:#BREQ
            self.lock.acquire()
            if self.acc == 0:
                self.setPC(opr)
            self.lock.release()
        elif opcode == 10:#IN
            self.lock.acquire()
            inputData = raw_input('> ')
            self.memory[self.translate(opr)] = inputData
            self.incrementPC()
            self.lock.release()
        elif opcode == 11:#OUT
            self.lock.acquire()
            print self.memory[self.translate(opr)]
            self.incrementPC()
            self.lock.release()
        elif opcode == 12:#STOP
            pass
        elif opcode == 13:#DAT
            pass
        else:
            print "opcode ", opcode, " invalid"