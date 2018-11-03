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
            return physicalPosition
        else:
            print "Improper access"

    def translate(self, logicalPosition):
        physicalPosition = self.r0+logicalPosition
        if self.validatePosition(physicalPosition):
            return physicalPosition
        else:
            print "Improper access"

    def validatePosition(self, position):
        if self.r0 <= physicalPosition and self.r1 >= physicalPosition:
            return True
        else:
            return False

    def execInstruction(self, opcode):
        if opcode == 1: #ADD
            pass
        elif opcode == 2:#SUB
            pass
        elif opcode == 3:#MUL
            pass            
        elif opcode == 4:#DIV
            pass
        elif opcode == 5:#LOAD
            pass
        elif opcode == 6:#STORE
            pass
        elif opcode == 7:#BRPOS
            pass
        elif opcode == 8:#BRNEG
            pass
        elif opcode == 9:#BREQ
            pass
        elif opcode == 10:#IN
            pass
        elif opcode == 11:#OUT
            pass
        elif opcode == 12:#STOP
            pass
        elif opcode == 13:#DAT
            pass
        else:
            print "opcode ", opcode, " invalid"