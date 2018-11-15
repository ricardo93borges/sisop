import os
import time
import random
import threading
from Pcb import Pcb
from MemoryManager import MemoryManager
from MemoryPosition import MemoryPosition

class Exec(threading.Thread):

    def __init__(self, memory, partitons, partitionLength, pcbs, readyProcesses):
        threading.Thread.__init__(self, group=None, target=None, name='EXEC',verbose=None)
        self.lock = threading.Lock()
        self.memory = memory
        self.partitions = partitons
        self.partitionLength = partitionLength
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.programsPath = self.path+"/../programs/"
        self.submittedList = self.path+"/submitted.txt"
        self.readyProcesses = readyProcesses
        self.pcbs = pcbs

    def run(self):
        print "Thread", self.getName()
        t = True
        while True:
            #check if there is any programs submitted
            submittedFile = open(self.submittedList, 'r')
            programs = submittedFile.readlines()
            submittedFile.close()
            #programs = ["p1.txt", "p2.txt", "p3.txt"]
            self.lock.acquire()
            for programName in programs:
                programName = programName.replace("\n","")
                
                #allocate a partition for the program
                mm = MemoryManager(self.memory, self.partitions, self.partitionLength)                
                partition = mm.allocMemory()
                print "program ", programName, ' allocated in partition:', partition

                if(type(partition) == bool and partition == False):
                    print 'Memory full'
                else:
                    #Create a PCB for the program
                    pcb = Pcb(random.randint(1000, 9999), 0, 0, partition, partition+self.partitionLength)
                    self.pcbs.append(pcb)
                    
                    #get program instruction from program file
                    programFile = open(self.programsPath+programName, 'r')
                    programInstructions = programFile.readlines()
                    programFile.close()

                    #translate program instructions and load it in memory
                    program = self.translateProgramInstruction(programInstructions)
                    mm.loadProgram(partition, program)

                    #Append program in ready list
                    self.readyProcesses.put(pcb.pid)                    

            submittedFile = open(self.submittedList, 'w')
            submittedFile.write("")
            submittedFile.close()
            
            self.lock.release()
            t = False
            time.sleep(1)

    #Translate a program instruction to a MemoryPosition instance
    def translateProgramInstruction(self, instructions):
        positionsArr = []
        for instruction in instructions:
            instruction = instruction.replace("\n","")
            instructionArr = instruction.split(" ")

            if instructionArr[0] == 'ADD':
                mp = MemoryPosition(1, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'SUB':
                mp = MemoryPosition(2, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'MUL':
                mp = MemoryPosition(3, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'DIV':
                mp = MemoryPosition(4, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'LOAD':
                mp = MemoryPosition(5, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'STORE':
                mp = MemoryPosition(6, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'BRPOS':
                mp = MemoryPosition(7, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'BRNEG':
                mp = MemoryPosition(8, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'BREQ':
                mp = MemoryPosition(9, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'IN':
                mp = MemoryPosition(10, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'OUT':
                mp = MemoryPosition(11, int(instructionArr[1]))
                positionsArr.append(mp)
            elif instructionArr[0] == 'STOP':
                mp = MemoryPosition(12, None)
                positionsArr.append(mp)
            elif instructionArr[0] == 'DAT':
                mp = MemoryPosition(13, int(instructionArr[1]))
                positionsArr.append(mp)
            else:
                print "Invalid instruction"
        
        return positionsArr
