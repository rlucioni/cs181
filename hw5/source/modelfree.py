from random import *
import throw
import darts
 
EXPLORE_TURNS = 5
EPSILON = 0.5

# The default player aims for the maximum score, unless the
# current score is less than the number of wedges, in which
# case it aims for the exact score it needs. 
#  
# You may use the following functions as a basis for 
# implementing the Q learning algorithm or define your own 
# functions.

def start_game():

  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES)) 

def get_target(score):

  if score <= throw.NUM_WEDGES: return throw.location(throw.SECOND_PATCH, score)
  
  return(throw.location(throw.INNER_RING, throw.NUM_WEDGES))

# Exploration/exploitation strategies below. Return 0 to exploit and 1 to explore (randomly). 

# Time-T Mode Switching
def ex_strategy_one(time):
  if time < EXPLORE_TURNS:
    return 1
  else:
    return 0

# Epsilon-Greedy
def ex_strategy_two(time):
  # decay epsilon over time
  if random.random() < EPSILON/time:
    return 1
  else:
    return 0


# The Q-learning algorithm:
def Q_learning():
  return
