'''
Created on 22 Oct 2015

@author: tobydobbs
'''

import ANN, ranker, activation, InputsOutputs, grapher
import random, copy, sys, matplotlib.pyplot as pl
from decimal import Decimal

#===============================================================================
# initPop: initialize the population
#===============================================================================
def initPop(size, noInputs, mi, mx):

    pop = []
    for i in range(size):
        toAdd = ANN.ANN(noInputs, 6, mi, mx)
        pop.append(toAdd)
    return pop

#===============================================================================
# buildOutputArray: construct a blank matrix to store output values
#===============================================================================
def buildOutputArray(noInputs, size):
    
    outputs = []
    for i in range(size):
        outputs.append([0] * noInputs)
    return outputs

#===============================================================================
# getOutputs: get the outputs given a set of inputs - generation-wise
#===============================================================================
def getOutputs(population, inputs):
    
    #complete one iteration - i.e. run each input through each MLP in the population and store the output
    outputs = buildOutputArray(len(inputs), len(population)) # the outputs of each neuron in each mlp
    for p in range(len(population)): # run each input through each MLP in the population
        for i in range(len(inputs)): # get the next input
            outputs[p][i] = population[p].go(inputs[i]) # push the input through each network and save the output
    return outputs

#===============================================================================
# getOutputs2: alternative for cases with 2 inputs
#===============================================================================
def getOutputs2(population, inputs):
    
    outputs = buildOutputArray(len(desOutputs), len(population)) # the outputs of each neuron in each mlp
    for p in range(len(population)):
        i = 0
        j = 0
        while i < len(desOutputs):
            outputs[p][i] = population[p].go(inputs[j], inputs[j+1])
            i += 1
            j += 2
    return outputs

def square(x):
    
    return x * x

#===============================================================================
# MSE: find the mean-squared error
#===============================================================================
def MSE(desOutputs, population, outputs):
    
    mses = [] # the mean standard errors of each mlp - synonymous with fitness
    for p in range(len(population)):
        summ = 0
        for d in range(len(desOutputs)):
            summ += square(desOutputs[d] - outputs[p][d]) / float(len(desOutputs))
        mses.append((p, summ))
    return mses # return a list of tuples (mlp-index, mse/fitness)

#===============================================================================
# rank: sort the list of mses from worst to best - the tuple records the position of the MLP in the population
#===============================================================================
def rank(mses):
    
    ranker.quickSort(mses, 0, len(mses)-1)
        
#===============================================================================
# findFittest: find the fittest member of a group of tuples (i.e. run a tournament) (mlp-index, fitness)
#===============================================================================
def findFittest(group):
    
    fittest = group[0]
    for member in group:
        if member[1] < fittest[1]:
            fittest = member
    return fittest[0]

#===============================================================================
# This function works in the following way:
# Iterate through the chromosomes of two parents, synchronously
# randomly select one value from the current position in each parent
# insert the randomly selected value in the same position in the child
# return the child
#===============================================================================
def crossover(parent1, parent2, mut_rate, noInputs, mi, mx):

    child = ANN.ANN(noInputs, 6, mi, mx)
    
    if weights == True:
        noRows = len(parent1.weights)
        
        for row in range(noRows):
            noCols = len(parent1.weights[row])
            for col in range(noCols):
                cur1 = parent1.weights[row][col] # current element in parent 1
                cur2 = parent2.weights[row][col] # current element in parent 2
                child.weights[row][col] = random.choice([cur1, cur2])
            
    if func == True: # the user can choose to cross over functions
        #print "crossing functions"
        child = crossFunctions(parent1, parent2, child)
       
    return child 

#===============================================================================
# crossFunctions: crossover functions, process same as above
#===============================================================================
def crossFunctions(parent1, parent2, child):
    
    for i in range(len(parent1.functions)):
        cur1 = parent1.functions[i]
        cur2 = parent2.functions[i]
        child.functions[i] = random.choice([cur1, cur2])
    return child
    

#===============================================================================
# mutation: select a gene at random and change the value
#===============================================================================
def mutation(member, mut_rate, mi, mx):
    
    if random.random() <= mut_rate:
        
        if weights == True:
            row = random.randint(0, len(member.weights)-1) # select a row at random
            column = random.randint(0, len(member.weights)-1) # select a column at random
            
            while member.weights[row][column] == 0:
                row = random.randint(0, len(member.weights)-1) 
                column = random.randint(0, len(member.weights)-1) 
                
            member.weights[row][column] = member.randomWeight(mi, mx)
        
        if func == True:
            member = mutFunctions(member)
            
    return member

#===============================================================================
# mutFunctions: mutate the individual's functions
#===============================================================================
def mutFunctions(member):
    
    # print "Mutating the functions"
    index = random.randint(0, len(member.functions)-1)
    member.functions[index] = activation.luckyDip()
    return member
    
#===============================================================================
# selectParents: obtain a collection of parents with which to breed children
#===============================================================================
def selectParents(mses):
    
    popsize = len(mses)
    parents = []
    for i in range(2 * (popsize - 1)):
        parents.append(rankSelect(mses))
    return parents

#===============================================================================
# rankSelect: selects a member of the array based on rank - fittest is most likely to be picked
#===============================================================================
def rankSelect(mses):
    
    popsize = len(mses)
    F = (popsize * (popsize + 1)) / 2
    
    i = Decimal(1)
    prev_prob = 0 # store the previous probability 
    selection = random.random() # choose random number for selection
    while selection > ((i / F) + prev_prob) and i <= popsize: # '<=' as ranks start at 1
        prev_prob += (i / F)
        i += 1
    return mses[int(i)-1][0] # return the index of the selected MLP

#===============================================================================
# pairUp: randomly pairs up selected parents to form couples
#===============================================================================
def pairUp(parents):
    
    couples = []
    for i in range(len(parents) / 2):
        mother = random.choice(parents)
        father = random.choice(parents)
        couples.append((mother, father))
    return couples

#===============================================================================
# breed: carry out one breeding step
#===============================================================================
def breed(pop, cross_rate, mut_rate, mi, mx, noInputs):
    
    if noInputs < 2:
        outputs = getOutputs(pop, inputs) # find the outputs of each MLP for each input
    else:
        outputs = getOutputs2(pop, inputs)
    
    mses = MSE(desOutputs, pop, outputs) # find the mses for the population
    rank(mses) # first rank the MSEs - i.e. order them from worst to best

    print "MSE: " + str(mses[len(mses)-1][1])
    array4.append(outputs[mses[len(mses)-1][0]]) # needed for graph plotting
    array2.append(mses[len(mses)-1][1])
    
    strongest = copy.deepcopy(pop[mses[len(mses)-1][0]]) # keep the strongest in the population
    children = [strongest]
    
    parents = selectParents(mses) # select parents for breeding
    couples = pairUp(parents)
    
    # this loop simulates the mating process - fills an array of children
    for couple in couples:
        mother = pop[couple[0]]
        father = pop[couple[1]]
        if random.random() <= cross_rate:
            newChild = crossover(mother, father, mut_rate, noInputs, mi, mx)
        else:
            newChild = random.choice([mother, father])
        children.append(mutation(newChild, mut_rate, mi, mx))
        
    return children

#===============================================================================
# Here the user specifies the desired function
#===============================================================================
function = raw_input("Which function?\n")
one = ["linear", "sine", "cubic", "tanh"]
two = ["xor", "complex"]
if(one.__contains__(function)):
    number = 1
elif(two.__contains__(function)):
    number = 2
else:
    raise "The function you have specified is not valid."

#===============================================================================
# Here the user specifies whether they wish to evolve functions/weights
#===============================================================================
func, weights = False, False
q1 = raw_input("Do you wish to evolve functions? (Y/N)\n")
if q1 == "N":
    weights = True
else:
    func = True
    q2 = raw_input("Do you wish to evolve weights? (Y/N)\n")
    if q2 == "Y":
        weights = True   

#===============================================================================
# Read the input file and store the input and output values in lists
#===============================================================================
io = InputsOutputs.IO("Data-tsv/" + str(number) + "in_" + function + ".tsv")
inputs = io.getInputs()
desOutputs = io.getOutput()

array2 = [] # store the mse
array4 = [] # store the actual output
    
#===============================================================================
# main: the main method of the program - user provides run configuration arguments
#===============================================================================
def main(pop_size, cross_rate, mut_rate, no_iter, noInputs, mi, mx):
    
    pop_size = int(pop_size)
    noInputs = int(noInputs)
    cross_rate = float(cross_rate)
    mut_rate = float(mut_rate)
    no_iter = int(no_iter)
    mi = float(mi)
    mx = float(mx)
    
    population = initPop(pop_size, noInputs, mi, mx) # obtain an initial population
    
    i = 1
    print "Generation " + str(i)
    nextGen = breed(population, cross_rate, mut_rate, mi, mx, noInputs)
    grapher.plotGraph(range(len(desOutputs)), array4.pop(), desOutputs)
    
    while i < no_iter:
        i += 1
        print "Generation " + str(i)
        nextGen = breed(nextGen, cross_rate, mut_rate, mi, mx, noInputs)
        grapher.plotGraph(range(len(desOutputs)), array4.pop(), desOutputs)
     
    nextGen[0].printFunctions()
    pl.ioff()  
    pl.show()
    pl.plot(array2) #plt the MSE curve
    pl.show()
        
    
if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6], sys.argv[7])
    