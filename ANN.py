'''
Created on 21 Oct 2015

@author: tobydobbs
'''
import activation, random, sys

#===============================================================================
# ANN: Each ANN object represents an individual MLP
#===============================================================================
class ANN:
    
    def __init__(self, noInputs, noNeurons, mi, mx):
        
        self.noInputs = noInputs;
        self.noNeurons = noNeurons;
        
        self.axons = {} # store the connections
        self.noAxons = 0 # keep a tab on connections
        
        self.weights = self.buildMatrix() # the axons in the network
        self.functions = self.assignFunctions() # the functions for each node
        
        self.outputs = [0] * (noInputs + noNeurons)
        
        self.addConnections() # adds the connections
        self.initialiseWeights(mi, mx) # randomize weights
        
    #===========================================================================
    # constructs a 8x8 matrix representing the weights of each connection - initially empty
    #===========================================================================
    def buildMatrix(self):
        indexes = self.noInputs + self.noNeurons
        matrix = []
        for i in range(indexes):
            matrix.append([0] * (indexes))    
        return matrix;
    
    #===========================================================================
    # add a new connection to the network
    #===========================================================================
    def addConnections(self):
        indexes = self.noInputs + self.noNeurons
        for i in range(self.noInputs, indexes-1): #only for the hidden layer(s)
            for n in range(self.noInputs):
                self.addAxon(n, i)
            self.addAxon(i, indexes - 1)
            
    #===========================================================================
    # summingJunction: acts as the summing junction for a neuron which the user specifies
    #===========================================================================
    def summingJunction(self, neuron):
        row = neuron #the column lists all of the inputs to that neuron (eg. column 2 for the thrid neuron)
        summ = 0
        for column in range(len(self.weights[row])):
            summ += self.weights[row][column] * self.outputs[column]
        return summ
    
    #===========================================================================
    # add a new axon to the network
    #===========================================================================
    def addAxon(self, fro, to):
        self.noAxons += 1
        self.axons[self.noAxons] = (fro, to)
        
    #===========================================================================
    # initialize each connection with a random weight
    #===========================================================================
    def initialiseWeights(self, mi, mx):
        if mi < -5 or mx > 5:
            print "The interval can only range from -5 to 5 inclusive"
            sys.exit(0)
        noRows = len(self.weights)
        for row in range(noRows):
            noCol = len(self.weights[row])
            for col in range(noCol):
                if (row, col) in self.axons.values():
                    self.weights[col][row] = self.randomWeight(mi, mx)
    
    #===========================================================================
    # assign a random activation function to each neuron
    #===========================================================================
    def assignFunctions(self):
        functions = []
        for i in range(self.noNeurons):   
            toAdd = activation.luckyDip()
            functions.append(toAdd)    
        return functions
    
    #===========================================================================
    # returns a random number between two boundaries - biased
    #===========================================================================
    def randomWeight(self, bottom, top):
        return random.uniform(bottom, top)
    
    #===========================================================================
    # go: this function should be called to start an epoch
    #===========================================================================
    def go(self, input1, input2 = None):
        #print "input 1: " + str(input1) + " input 2: " + str(input2)
        self.outputs[0] = input1
        if input2 != None:
            self.outputs[1] = input2
        
        for i in range(self.noInputs, len(self.weights)):
            self.outputs[i] = self.functions[i-self.noInputs](self.summingJunction(i))
        
        return self.outputs[len(self.weights)-1];      
    
    #------------------------------------------------------------------------------ 
    
    def printWeights(self): 
        print "The weights of the MLP"
        noRows = len(self.weights)
        for row in range(noRows):  
            print self.weights[row]
                
    def printFunctions(self):
        print "The functions of the MLP"
        for f in range(len(self.functions)):
            print "N" + str(f) + ": " + str(self.functions[f]) 
 
#===========================================================================
# main method used for testing - not called elsewhere
#===========================================================================
def main():
    ann = ANN(2, 6)
    
    ann.printWeights()
    ann.printFunctions()
    
    print ann.go(4,2)
    
if __name__ == "__main__":
    main()
