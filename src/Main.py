from Cpu import Cpu
from MemoryPosition import MemoryPosition

class Main:

    partitions = 16
    partitionLength = 64
    memoryLength = partitions * partitionLength
    memory = [None]*memoryLength

    def __init__(self):
        print "main"
        print len(Main.memory)
        #cpu = Cpu()
        #cpu.start()

main = Main()        