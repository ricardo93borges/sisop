import os 

class Shell():

    def __init__(self):
        self.path = os.path.dirname(os.path.realpath(__file__))
        self.submittedList = self.path+"/submitted.txt"
        print self.submittedList

    def run(self):
        while True:
            print "Enter a program name"
            program = raw_input('> ')
            file = open(self.submittedList, 'a')
            file.write(program+"\n")
            file.close()            

shell = Shell()
shell.run()            