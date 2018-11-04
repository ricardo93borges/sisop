from Cpu import Cpu
from Exec import Exec
from MemoryPosition import MemoryPosition

class Main:

    partitions = 16
    partitionLength = 64
    memoryLength = partitions * partitionLength
    memory = [None]*memoryLength

    def __init__(self):
        print "main"
        #print Main.memory

        cpu = Cpu(Main.memory)
        ex = Exec(Main.memory, Main.partitions, Main.partitionLength)

        cpu.start()
        ex.start()



main = Main()        