import os
import time
import random
import threading
from Pcb import Pcb
from MemoryManager import MemoryManager
from MemoryPosition import MemoryPosition

class Exec(threading.Thread):

    def __init__(self, memory, partitons, partitionLength):
        threading.Thread.__init__(self, group=None, target=None, name='EXEC',verbose=None)
        self.lock = threading.Lock()
        self.memory = memory
        self.partitions = partitons
        self.partitionLength = partitionLength
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.programsPath = self.path+"/../programs/"
        self.submittedList = self.path+"/submitted.txt"
        self.readyList = self.path+"/ready.txt"

    def run(self):
        print "Thread", self.getName()
        while True:
            #check if there are programs submitted
            submittedFile = open(self.submittedList, 'r')
            programs = submittedFile.readlines()
            submittedFile.close()
            
            self.lock.acquire()
            for programName in programs:
                programName = programName.replace("\n","")
                print "program name", programName

                #allocate a partition for the program
                mm = MemoryManager(self.memory, self.partitions, self.partitionLength)                
                partition = mm.allocMemory()

                if(type(partition) == bool and partition == False):
                    print 'Memory full'
                else:
                    #TODO store pcb in a list of pcbs
                    #print partition, self.partitionLength
                    pcb = Pcb(random.randint(1000, 9999), 0, 0, partition, partition+self.partitionLength)
                    
                    #get program instruction from program file
                    programFile = open(self.programsPath+programName, 'r')
                    programInstructions = programFile.readlines()
                    programFile.close()

                    #translate program instructions and load it in memory
                    program = self.translateProgramInstruction(programInstructions)
                    mm.loadProgram(partition, program)

                    #update ready list
                    readyFile = open(self.readyList, 'a')
                    readyFile.write(programName+"\n")
                    readyFile.close()

                    #print self.memory

            submittedFile = open(self.submittedList, 'w')
            submittedFile.write("")
            submittedFile.close()
            
            self.lock.release()            
            time.sleep(1)

    def translateProgramInstruction(self, instructions):
        positionsArr = []
        for instruction in instructions:
            instruction = instruction.replace("\n","")
            instructionArr = instruction.split(" ")

            if instructionArr[0] == 'ADD':
                mp = MemoryPosition(1, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'SUB':
                mp = MemoryPosition(2, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'MUL':
                mp = MemoryPosition(3, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'DIV':
                mp = MemoryPosition(4, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'LOAD':
                mp = MemoryPosition(5, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'STORE':
                mp = MemoryPosition(6, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'BRPOS':
                mp = MemoryPosition(7, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'BRNEG':
                mp = MemoryPosition(8, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'BREQ':
                mp = MemoryPosition(9, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'IN':
                mp = MemoryPosition(10, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'OUT':
                mp = MemoryPosition(11, instructionArr[1])
                positionsArr.append(mp)
            elif instructionArr[0] == 'STOP':
                mp = MemoryPosition(12, None)
                positionsArr.append(mp)
            else:
                print "Invalid instruction"
        
        return positionsArr
