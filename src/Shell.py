import threading

class Shell(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self, group=None, target=None, name='SHELL',verbose=None)

    def run(self):
        print "Thread", self.getName()