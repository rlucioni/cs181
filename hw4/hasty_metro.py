import matplotlib.pyplot as plt
import numpy as np
from pylab import *
import random
import utils

plt.clf()
hit = 0
canidate = 0
data = [] 
where_we_at = 0
acceptance_ratio = 0
func = lambda x: .2*utils.norm(x, 1,25) + .3*utils.norm(x, -2,1) + .5*utils.norm(x, 3,4)

for i in range(1000):
    canidate = random.gauss(where_we_at,3)
    acceptance_ratio = func(canidate)/func(where_we_at) 
    
    if (acceptance_ratio >=1):
        #auto accept
        if (i >= 500):
            hit += 1
            data.append(canidate)
        where_we_at = canidate

    else:
        if (random.uniform(0,1) <= acceptance_ratio):
            #accept
            if (i >= 500):
                hit += 1
                data.append(canidate)
            where_we_at = canidate
        else:
            #reject
            if (i >= 500):
                data.append(where_we_at)

print hit
hist, bins = np.histogram(data,bins = 50, density=True)
width = 0.7*(bins[1]-bins[0])
center = (bins[:-1]+bins[1:])/2
plt.bar(center, hist, align = 'center', width = width)
#savefig('hasty_metro_histogram.pdf')
