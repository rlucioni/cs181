import math


#Cumulative Distribution Function
#P (X<=x) = 1/2 erfc((mu-x)/(sqrt(2) sigma))
def cdf(mu, sigma): return lambda x: (1/2)* math.erfc((mu-x) / (sigma * math.sqrt(2)))

#Normal Distribution (Gaussian Distribution)
#e^(-(x-mu)^2/(2 sigma^2))/(sqrt(2 pi) sigma)
def norm(mu,var):
    sigma = math.sqrt(var)
    return lambda x: exp((-(x-mu)^2)/(2*var))/(math.sqrt(2*pi)*sigma)


