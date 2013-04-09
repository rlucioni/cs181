import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import random

plt.clf()

data = []

for i in range(500):
    toss = random.randrange(1,10,1)
    if toss == 1 or toss == 2:
        data.append(.2*random.gauss(1,5)) 
    if toss == 3 or toss == 4 or toss == 5:
        data.append(.3*random.gauss(-2,1))
    else:
        data.append(.5*random.gauss(3,2))

hist, bins = np.histogram(data,bins = 50)
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2
plt.bar(center, hist, align = 'center', width = width)
savefig('direct-sample-histogram-1.pdf')
