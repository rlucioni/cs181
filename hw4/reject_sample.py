import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import random
import utils
import math

plt.clf()
hit = 0
miss = 0
val = 0
yval = 0
data = [] 

mixture = lambda x: .2*utils.norm(x,1,25) + .3*utils.norm(x,-2,1) + .5*utils.norm(x,3,4)
upper_bound = lambda x: 2*utils.norm(x,0,24)

while (hit < 500):
    val = random.gauss(0,math.sqrt(24))
    yval = random.uniform(0,upper_bound(val))
    
    if (yval < mixture(val)):
        hit += 1
        data.append(val)

    else:
        miss += 1

print "HITS: {}".format(hit)
print "MISSES: {}".format(miss)

hist, bins = np.histogram(data,bins=50,density=True)
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2
plt.bar(center, hist, align = 'center', width = width)
#savefig('rejection-sample-histogram.pdf')
