'''
Created on 18 Oct 2015

@author: tobydobbs
'''
#===============================================================================
# Each function represents a separate activation function for use in the MLP
#===============================================================================

import math, random

#===============================================================================
# testFunc: used when testing initial designs
#===============================================================================
def testFunc(x):
    return x

def nullFunc(x):
    return 0;

def sigmoid(x):
    return 1 / (1 + math.exp(-x))

def tanh(x):
    return math.tanh(x)

def cosine(x):
    return math.cos(x)

def gaussian(x):
    return math.exp(-((x * x) / 2))

#===============================================================================
# luckyDip: select at random a function from those available to the network
#===============================================================================
def luckyDip():
    functions = [nullFunc, sigmoid, tanh, cosine, gaussian]
    return random.choice(functions)


def main():
    print cosine(30)
    
if __name__ == "__main__":
    main()
