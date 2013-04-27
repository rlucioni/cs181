import matplotlib.pyplot as plt
from pylab import *

plt.clf()

# these must have the same dimension
# number of clusters (K)
#xs = range(1,16)
xs = [3,10,100]

# Performance (average num throws)

#Time-T Mode Switching
#ys = [17.1333333333, 17.1333333333, 19.0, 15.2666666667, 16.0666666667, 16.2666666667, 18.4, 13.4, 15.1333333333, 17.6666666667, 16.7333333333, 17.2666666667, 15.7333333333, 19.8, 18.2]
ys = [15.85, 15.9, 17.32]

#Epsilon-Greedy
#ys = [14.4, 16.3333333333, 15.6, 15.3333333333, 21.6, 13.2, 19.2, 14.0666666667, 20.0, 15.2, 15.2666666667, 16.7333333333, 15.8666666667, 14.7333333333, 17.4666666667]
zs = [16.38, 16.12, 16.94]

p1, = plt.plot(xs, ys, color='b')
p2, = plt.plot(xs, zs, color='r')

plt.grid(b=1)

plt.title('Performance vs. Epoch Size')
plt.xlabel('Epoch Size')
plt.ylabel('Performance')
plt.axis([0,101,15,18])
plt.legend((p1,p2), ('Time-T Mode Switching','Epsilon-Greedy'), 'lower right')

# save figure as a pdf
#savefig('perf-v-epoch-mode-switch.pdf')
#savefig('perf-v-epoch-greedy.pdf')
savefig('perf-v-epoch-size.pdf')
