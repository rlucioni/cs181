import matplotlib.pyplot as plt
from pylab import *

plt.clf()

# these must have the same dimension
xs = range(1,31) # simple network
#xs = range(1,20) # 15 hidden units
#xs = range(1,29) # 30 hidden units


### TRAINING ERROR ###

# simple network
ys = [0.44322222, 0.38988889, 0.37377778, 0.36511111, 0.36155556, 0.36077778, 0.36011111, 0.35900000, 0.35877778, 0.35844444, 0.35911111, 0.35933333, 0.35922222, 0.35866667, 0.35844444, 0.35822222, 0.35833333, 0.35855556, 0.35855556, 0.35855556, 0.35877778, 0.35888889, 0.35877778, 0.35877778, 0.35877778, 0.35888889, 0.35888889, 0.35888889, 0.35900000, 0.35900000]

### VALIDATION ERROR ####

# simple network
zs = [0.482, 0.428, 0.403, 0.401, 0.397, 0.393, 0.389, 0.392, 0.390, 0.388, 0.387, 0.387, 0.387, 0.385, 0.385, 0.384, 0.385, 0.385, 0.385, 0.385, 0.385, 0.385, 0.385, 0.385, 0.385, 0.384, 0.384, 0.384, 0.384, 0.384]

### TEST ERROR ###
qs = [0.443, 0.381, 0.383, 0.372, 0.365, 0.360, 0.355, 0.354, 0.355, 0.353, 0.352, 0.353, 0.352, 0.352, 0.353, 0.353, 0.353, 0.353, 0.353, 0.353, 0.355, 0.354, 0.354, 0.354, 0.354, 0.354, 0.354, 0.354, 0.354, 0.354]

p1, = plt.plot(xs, ys, color='r')
p2, = plt.plot(xs, zs, color='g')
p3, = plt.plot(xs, qs, color='b')

plt.grid(b=1)

### SIMPLE NETWORK
plt.title('Simple Network, Learning Rate = 0.1')
plt.xlabel('Epochs')
plt.ylabel('Error')
plt.axis([0,31,0.00,0.45])
plt.legend((p1,p2,p3,), ('Training', 'Validation', 'Test'), 'lower right')

# save figure as a pdf
#savefig('Simple-Network-alpha-0_1.pdf')

### 15 HIDDEN UNITS
#plt.title('15 Hidden Units, Learning Rate = 1.0')
#plt.xlabel('Epochs')
#plt.ylabel('Error')
#plt.axis([0,20,0.00,0.55])
#plt.legend((p1,p2,), ('Training', 'Validation',), 'lower right')

# save figure as a pdf
#savefig('15-hidden-units-alpha-1_0.pdf')

### 30 HIDDEN UNITS
#plt.title('30 Hidden Units, Learning Rate = 0.1')
#plt.xlabel('Epochs')
#plt.ylabel('Error')
#plt.axis([0,29,0.00,0.95])
#lt.legend((p1,p2,), ('Training', 'Validation',), 'upper right')

# save figure as a pdf
savefig('simple-network-alpha-0_1.pdf')
