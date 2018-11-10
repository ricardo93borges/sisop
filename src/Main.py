from Ecpu import Ecpu
from Exec import Exec
from Console import Console
from MemoryPosition import MemoryPosition

class Main:

    partitions = 16
    partitionLength = 64
    memoryLength = partitions * partitionLength
    memory = [None]*memoryLength
    pcbs = []
    consoleRequests = ['123_out_hello world', '124_in_1']
    readyProcesses = []

    def __init__(self):
        print "main"
        #print Main.memory

        #ecpu = Ecpu(Main.memory, Main.consoleRequests)
        ex = Exec(Main.memory, Main.partitions, Main.partitionLength, Main.pcbs, Main.readyProcesses)
        #console = Console(Main.memory, Main.consoleRequests)

        #ecpu.start()
        ex.start()
        #console.start()

main = Main()        