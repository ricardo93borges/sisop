from Cpu import Cpu
from MemoryPosition import MemoryPosition

class Main:

    partitions = 16
    partitionLength = 64
    memoryLength = partitions * partitionLength
    memory = [None]*10

    def __init__(self):
        print "main"
        print Main.memory
        cpu1 = Cpu(Main.memory)
        cpu1.start()        

main = Main()        