'''
Created on 27 Oct 2015

@author: tobydobbs
'''

import matplotlib.pyplot as plt

plt.ion()
fig = plt.figure(1)
ax1 = fig.add_subplot(111)

def plotGraph(x, y, b):   
    ax1.plot(x, y, '-', x, b , '-')
    plt.draw() 
    ax1.clear()  