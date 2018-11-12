from Ecpu import Ecpu
from Exec import Exec
from Console import Console
from MemoryPosition import MemoryPosition
import Queue

class Main:

    partitions = 16
    partitionLength = 64
    memoryLength = partitions * partitionLength
    memory = [None]*memoryLength
    pcbs = []
    consoleRequests = Queue.Queue()
    readyProcesses = Queue.Queue()

    def __init__(self):
        print "main"
        #print Main.memory
        
        ecpu = Ecpu(Main.memory, Main.consoleRequests, Main.readyProcesses, Main.pcbs)
        ex = Exec(Main.memory, Main.partitions, Main.partitionLength, Main.pcbs, Main.readyProcesses)
        console = Console(Main.memory, Main.consoleRequests, ecpu)
        
        console.start()
        ecpu.start()
        ex.start()

main = Main()        