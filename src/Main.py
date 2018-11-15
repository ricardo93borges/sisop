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
    pcbs = [] #store PCBs
    consoleRequests = Queue.Queue() #store Console requests, Queue is thread safe
    readyProcesses = Queue.Queue() #store ready processes, Queue is thread safe

    def __init__(self):
        print "main"
        
        ecpu = Ecpu(Main.memory, Main.consoleRequests, Main.readyProcesses, Main.pcbs)
        ex = Exec(Main.memory, Main.partitions, Main.partitionLength, Main.pcbs, Main.readyProcesses)
        console = Console(Main.memory, Main.consoleRequests, ecpu)
        
        console.start()
        ecpu.start()
        ex.start()

main = Main()        