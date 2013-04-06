import matplotlib.pyplot as plt
import numpy as np
import matplotlib.mlab as mlab
import utils
from pylab import *

#NormalDistribution[1, 25]) + (0.3*NormalDistribution[-2, 1])+(0.05*NormalDistribution[3, 4])
factor1 = .02
mean1 = 1
variance1 = 2
sigma1 = sqrt(variance1)

factor2 = .03
mean2 = -2
variance2 = 1
sigma2 = sqrt(variance2)

factor3 = .05
mean3 = 3
variance3 = 4
sigma3 = sqrt(variance3)

x = np.linspace(-7,10,100)

func1 =factor1* mlab.normpdf(x,mean1,sigma1)

cdf1 = cdf(mean1, sigma1)
plt.plot(x,cdf1)

#intg1 = factor1*mlab.normpdf(x,mean1,sigma1)*(-(x-mean1)/variance1)


func2 =factor2* mlab.normpdf(x,mean2,sigma2)
func3 =factor3* mlab.normpdf(x,mean3,sigma3)
#plt.plot(x,func1+func2+func3)
plt.plot(x,mlab.normpdf(x,mean1,sigma1))
#plt.plot(x,intg1)

plt.show
savefig('test.pdf')
#savefig('mixture_o_gaussians.pdf')