import matplotlib.pyplot as plt
from pylab import *

plt.clf()

# these must have the same dimension
xs = range(5)
ys = [.3, .5, .1, .8, 1]
zs = [.6, .4, .0, .07, .9]

p1, = plt.plot(xs, ys, color='b')
p2, = plt.plot(xs, zs, color='r')

plt.title('Performance on Non-Noisy Data')
# plt.title('Performance on Noisy Data')
plt.xlabel('Validation Set Size')
plt.ylabel('Predictive Accuracy')
plt.axis([0,4,0,1])
plt.legend((p1,p2,), ('Training Accuracy', 'Test Accuracy',), 'lower right')

# save figure as a pdf
savefig('figure.pdf')
