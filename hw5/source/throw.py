from math import *
from random import *

# Parameters of a dartboard.
# NUM_WEDGES is simply the number of different wedges around the board.
# WEDGES is the list of wedges, in counter-clockwise order, beginning
# with the rightmost edge (angle 0).

### The standard dartboard #
##NUM_WEDGES = 20
##wedges = [6, 13, 4, 18, 1, 20, 5, 12, 9, 14, 11, 8, 16, 7, 19, 3, 17, 2, 15, 10]
##START_SCORE = 301

# A medium-size dartboard #
##NUM_WEDGES = 8
##wedges = [ 4, 6, 2, 7, 1, 8, 3, 5 ]
##START_SCORE = 100

# A much smaller dartboard #
NUM_WEDGES = 4
wedges = [ 1, 4, 2, 3 ]
START_SCORE = 9

angles = []



# A location on a dartboard consists of the wedge number, and a ring.
# Wedges are numbered from 1 to 20 IN THE STANDARD CASE ONLY. Rings are as ALWAYS follows.
CENTER, INNER_RING, FIRST_PATCH, MIDDLE_RING, SECOND_PATCH, OUTER_RING, MISS = \
        range(7)
    

class location:
    def __init__(self, _ring, _wedge):
        self.ring = _ring
        self.wedge = _wedge

# Initialize the wedges and angles arrays #/


def init_board():
   # angles = []
    
    for i in range(NUM_WEDGES):
        angles.append(None)
    angles.append(None)
    for i in range(NUM_WEDGES):
        j = wedges[i]
        angles[j] = i

# Determine the raw score for a board location #/

def location_to_score(loc):
    ring = loc.ring
    if ring == CENTER:
        result = 2.5 * NUM_WEDGES
    elif ring == INNER_RING:
        result = 1.25 * NUM_WEDGES
    elif ring == FIRST_PATCH:
        result = loc.wedge
    elif ring == MIDDLE_RING:
        result = 3 * loc.wedge
    elif ring == SECOND_PATCH:
        result = loc.wedge
    elif ring == OUTER_RING:
        result = 2 * loc.wedge
    else:
        result = 0

    return result

#
 # The throwing model takes as input a target location.  
 # It proceeds as follows:
 # (1) Convert the dartboard location into a geometric location in polar coordinates.
 # (2) Convert the polar coordinates into rectangular coordinates.
 # (3) Add bias and noise to the rectangular coordinates.
 # (4) Convert back into polar coordinates.
 # (5) Convert back into a dartboard location, and return.
 #
 # The bias is a constant factor added to each throw, modeling consistent
 # tendencies of a thrower to aim incorrectly.
 # The noise is an added jitter factor randomly added to a throw, modeling
 # tendencies of a thrower to wobble.
 #
 # A thrower is therefore characterized by the bias and the degree of wobble.
 # These are captured in the bias and wobble variables, which are set randomly
 # by init_thrower. 
 #
 # A simpler throwing model is also provided.
 # In this model, the wedge hit is distributed as follows: 
 # With probability 0.1: two to the left of the target wedge
 # With probability 0.2: one to the left of the target wedge
 # With probability 0.4: the target wedge
 # With probability 0.2: one to the right of the target wedge
 # With probability 0.1: two to the right of the target wedge
 # 
 # The ring hit is similarly distributed.  Let the target ring be i.
 # An error from -2 to +2 is selected, with probabilities as above.
 # The result ring is abs(i+error).
 #



    #1.
    # Determine the parameters of the throwing model.
    # The bias is drawn from a normal distribution, 
    # whose standard deviation is given by the constant BIAS_SD.
    # The wobble is uniform, in the range WOBBLE_MIN to WOBBLE_MAX.
    #
class TGlobals:
    BIAS_SD = 0.3
    WOBBLE_MIN = 0.5
    WOBBLE_MAX = 0.8
    bias = None
    wobble = None
    simple_flag = 0

def init_thrower():
    TGlobals.simple_flag = 0
    b = box_muller()
    
    bias_x = b.x * TGlobals.BIAS_SD
    bias_y = b.y * TGlobals.BIAS_SD
    wobble_x = TGlobals.WOBBLE_MIN + ranf()  * (TGlobals.WOBBLE_MAX - TGlobals.WOBBLE_MIN)
    wobble_y = TGlobals.WOBBLE_MIN + ranf()  * (TGlobals.WOBBLE_MAX - TGlobals.WOBBLE_MIN)

    TGlobals.bias = Rectangular(bias_x, bias_y)
    TGlobals.wobble = Rectangular(wobble_x, wobble_y)
    
    print "Thrower Bias:", bias_x, bias_y
    print "Thrower wobble:", wobble_x, wobble_y

def throw(target):
    if(TGlobals.simple_flag == 1):
        return simple_throwing_model(target)
    else:
        pol1 = location_to_polar(target)
        rect1 = polar_to_rectangular(pol1)
        rect2 = throwing_model(rect1)
        pol2 = rectangular_to_polar(rect2)
        result = polar_to_location(pol2)

        return result;
        
def use_simple_thrower():
    TGlobals.simple_flag = 1


def simple_throwing_model(target):
    e1 = rane()
    e2 = rane()
    angle1 = angles[target.wedge]
    angle2 = angle1 + e1
    
    angle3 = angle2 % NUM_WEDGES
    
    wedge = wedges[angle3]
    
    ring = abs(target.ring + e2)
    if(ring > MISS):
       ring = MISS

    return location(ring, wedge)

def throwing_model(rect):
    noise = box_muller()
    x = rect.x + TGlobals.bias.x + noise.x * TGlobals.wobble.x
    y = rect.y + TGlobals.bias.y + noise.y * TGlobals.wobble.y
    return Rectangular(x,y)

    

class Polar:
    def __init__(self, init_theta, init_r):
        self.theta = init_theta
        self.r = init_r

class Rectangular:
    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y


def rectangular_to_polar(rect):
    r = sqrt(rect.x * rect.x + rect.y * rect.y)
    theta = atan2(rect.y, rect.x)
    if(theta < 0):
        theta = theta + 2 * pi
    return Polar(theta, r)


def polar_to_rectangular(pol):
    y = pol.r * sin(pol.theta)
    x = pol.r * cos(pol.theta)
    return Rectangular(x,y)

# Convert between dartboard locations and polar coordinates #

def location_to_polar(loc):
    
    theta = angles[loc.wedge] * 2 * pi / NUM_WEDGES
    ring = loc.ring
    if ring == CENTER:
        r = 0
    elif ring == INNER_RING:
        r = 0.3
    elif ring == FIRST_PATCH:
        r = 1.1
    elif ring == MIDDLE_RING:
        r = 1.9
    elif ring == SECOND_PATCH:
        r = 2.5
    elif ring == OUTER_RING:
        r = 3.1
    else: r = 999999
    return Polar(theta, r)


def polar_to_location(pol):
    r = pol.r
    scaled_angle = (pol.theta * NUM_WEDGES) / (2 * pi)
    adjusted_angle = int(scaled_angle + 0.5) % NUM_WEDGES
    wedge = wedges[int(adjusted_angle)]

    if ( r < 0.2):
        ring = CENTER
    elif( r < 0.4):
        ring = INNER_RING
    elif (r < 1.8 ) :
        ring = FIRST_PATCH
    elif (r < 2.0 ) :
        ring = MIDDLE_RING
    elif (r < 3.0):
        ring = SECOND_PATCH
    elif (r < 3.2):
        ring = OUTER_RING
    else:
        ring = MISS

    return location(ring, wedge)


# Generate a uniform [0,1] random number #

def ranf():
    return uniform(0,1)

# 
 # Generate a random integer error from -2 to 2 with the probabilities
 # 0.1 : -2
 # 0.2 : -1
 # 0.4 : 0
 # 0.2 : 1
 # 0.1 : 2
 #
def rane():
    f = ranf()
    if (f<0.1):
        return -2
    elif (f<0.3): 
        return -1
    elif (f<0.7): 
        return 0
    elif (f<0.9): 
        return 1
    else: 
        return 2

# Generate two independent standard normal random numbers #
def box_muller():
    x = normalvariate(0,1)
    y = normalvariate(0,1)
    return Rectangular(x,y)
