'''
Created on 29 Oct 2015

@author: tobydobbs
'''

import csv

class IO:
    
    def __init__(self, file_name):
        self.input_array = []
        self.output_array = []

        self.readIn(file_name)
    
    def readIn(self, file_name):
        with open(file_name, 'rb') as tsvin:
            tsvin = csv.reader(tsvin, delimiter = '\t')
            
            for row in tsvin:
                if len(row) == 2: # check to see whether there are 1 or 2 inputs
                    self.input_array.append(float(row[0]))
                    self.output_array.append(float(row[1]))
                else:
                    self.input_array.append(float(row[0]))
                    self.input_array.append(float(row[1]))
                    self.output_array.append(float(row[2]))
                
                
    def getInputs(self):
        return self.input_array
    
    def getOutput(self):
        return self.output_array
    