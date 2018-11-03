import threading

class Cpu(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, group=None, target=None, name='CPU',verbose=None)

    def run(self):
        print "Thread", self.getName()