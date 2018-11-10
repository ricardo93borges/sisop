class MemoryManager():

    def __init__(self, memory, partitons, partitionLength):
        self.memory = memory
        self.partitions = partitons
        self.partitionLength = partitionLength
        self.memorySize = partitons*partitionLength

    def allocMemory(self):
        n = 0
        while(n <= self.memorySize):
            if n >= self.memorySize:                
                return False
            elif self.memory[n] == None:                
                return n            
            else:
                n += self.partitions

    def loadProgram(self, partition, program):
        if len(program) > self.partitionLength:
            print "program size is larger than a memory partition length"
        else:
            for instruction in program:
                self.memory[partition] = instruction
                partition += 1
