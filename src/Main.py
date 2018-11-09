from Cpu import Cpu
from Exec import Exec
from Console import Console
from MemoryPosition import MemoryPosition

class Main:

    partitions = 16
    partitionLength = 64
    memoryLength = partitions * partitionLength
    memory = [None]*10
    pcbs = []
    consoleRequests = ['123_out_hello world', '124_in_1']

    def __init__(self):
        print "main"
        #print Main.memory

        cpu = Cpu(Main.memory, Main.consoleRequests)
        ex = Exec(Main.memory, Main.partitions, Main.partitionLength, Main.pcbs)
        console = Console(Main.memory, Main.consoleRequests)

        cpu.start()
        ex.start()
        console.start()

main = Main()        