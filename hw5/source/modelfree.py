#from random import *
import random
import throw
import darts
import copy
 
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
def Q_learning(gamma, alpha, num_games):
  
# set these to values that make sense!
  #alpha = .5
  #gamma = .3

  Q = {}
  states = darts.get_states()
  actions = darts.get_actions()
  
  num_iterations = 0

  def lookup_max_a(state):
    cur_val = 0
    cur_index = -1
    for a in range(len(actions)):
      curent = Q[state][a]
      if curent > cur_val:
        cur_val = curent
        cur_index = a
    return cur_index
  
  # Initialize all the Q values to zero
  for s in range(len(actions)):
    Q[s]= {}
    for a in range(len(actions)):
        Q[s][a] = 0

   
  for g in range(1, num_games + 1):
    print "GAME {}".format(g)
    # run a single game
    s = throw.START_SCORE
    while s > 0:
      num_iterations += 1
      # The following two statements implement two exploration-exploitation
      # strategies. Comment out the strategy that you wish not to use.
 	  
      to_explore = ex_strategy_one(num_iterations)
      
      #to_explore = ex_strategy_two(num_iterations)
      if to_explore:
     	#explore
        a = random.randint(0, len(actions)-1)
        action = actions[a]
      else:
        # exploit
        a = lookup_max_a(s)
        action = actions[a]


      # Get result of throw from dart thrower; update score if necessary
      loc = throw.throw(action) 
      #should reward be based on action of loc?
      reward = darts.R(s,action) 
      s_prime = s - throw.location_to_score(loc)
      if s_prime < 0:
        s_prime = s
                
      # now we update the q score table
      #CONSIDER: is a copy call needed here?
      oldQ = copy.deepcopy(Q[s][a])
      nextQ = lookup_max_a(s_prime)
      #newQ = oldQ + alpha(reward + gamma(nextQ) - Q[s][a])
      newQ = oldQ + alpha(reward + gamma(Q[s][nextQ]) - oldQ)
      Q[s][a] = newQ
      s = s_prime

  print "Average turns = ", float(num_iterations)/float(num_games)

