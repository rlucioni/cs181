import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import random
import utils

plt.clf()
hit = 0
miss = 0
val = 0
yval = 0
data = [] 

func = lambda x: .2*utils.norm(1,25) + .3*utils.norm(-2,1) + .5*utils.norm(3,4)

while (hit < 500):
    val = random.gauss(0,24)
    yval = random.uniform(0,2*val)
    
    if (yval <= func(val)):
        hit += 1
        print "hit: {}".format(hit)
        data.append(val)

    else:
        miss += 1
        print "miss: {}".format(miss)

print miss
print hit
hist, bins = np.histogram(data,bins = 50)
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2
plt.bar(center, hist, align = 'center', width = width)
savefig('rejection-sample-histogram.pdf')
