import math


#Cumulative Distribution Function
#P (X<=x) = 1/2 erfc((mu-x)/(sqrt(2) sigma))
def cdf(mu, sigma,x):
    return (lamda x: (1/2)* erfc((mu-x) / (sigma * sqrt(2))))

#Normal Distribution (Gaussian Distribution)
#e^(-(x-mu)^2/(2 sigma^2))/(sqrt(2 pi) sigma)
def norm(mu,var,x):
    sigma = sqrt(var)
    return (lamda x: exp((-(x-mu)^2)/(2*var))/(sqrt(2*pi)*sigma))


