import matplotlib.pyplot as plt
from pylab import *

plt.clf()

# these must have the same dimension
# number of clusters (K)
xs = range(1,11)
# MSE
#ys = [1.97360905671, 1.74778748234, 1.65399446656, 1.45009995433, 1.33467421783, 1.44166487051, 1.2661665223, 1.25232064349, 1.26522099893, 1.15731114013]
#ys = [1.97360905671, 1.88100151706, 1.64963377791, 1.53424314422, 1.49196558677, 1.26277282488, 1.31338526986, 1.29026389502, 1.22227876667, 1.18138043207]

# neither of the above was great, so i averaged them!
ys = [(a+b)/2 for a,b in zip([1.97360905671, 1.74778748234, 1.65399446656, 1.45009995433, 1.33467421783, 1.44166487051, 1.2661665223, 1.25232064349, 1.26522099893, 1.15731114013], [1.97360905671, 1.88100151706, 1.64963377791, 1.53424314422, 1.49196558677, 1.26277282488, 1.31338526986, 1.29026389502, 1.22227876667, 1.18138043207])]

p1, = plt.plot(xs, ys, color='b')

plt.grid(b=1)

plt.title('Mean Squared Error vs. K, 1000 Examples')
plt.xlabel('K')
plt.ylabel('Mean Squared Error')
plt.axis([0,11,0,2.2])
#plt.legend((p1), ('Training Accuracy',), 'lower right')

# save figure as a pdf
savefig('mse-vs-k.pdf')
