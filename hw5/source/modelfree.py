#from random import *
import random
import throw
import darts
import copy
 
EXPLORE_TURNS = 10000
EPSILON = 5



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

def ex_strategy_three(game, totalgames):
  # decay epsilon over time
  if (float(game)/float(totalgames) < .5):
    return 1
  else:
    return 0


def lookup_max_a(Q_table,state,actions):
  cur_val = 0
  action = actions[0]
  for a in actions:
    curent = Q_table[state][a]
    if curent >= cur_val:
      cur_val = curent
      action = a
  return action

# The Q-learning algorithm:
def Q_learning(gamma, alpha, num_games):
  
# set these to values that make sense!
  #alpha = .5
  #gamma = .3

  Q = {}
  states = darts.get_states()
  actions = darts.get_actions()
  
  num_iterations = 0
  
  num_total_iterations = 1
  # Initialize all the Q values to zero
  for s in states:
    Q[s]= {}
    for a in actions:
        Q[s][a] = 0
   
  for g in range(1, num_games + 1):
    #print "Average turns = ", float(num_iterations)/float(g)
    #print "GAME {}".format(g)
    # run a single game
    s = throw.START_SCORE
    gamethrows = 0;
    while s > 0:
      num_total_iterations += 1  
      gamethrows += 1
      # The following two statements implement two exploration-exploitation
      # strategies. Comment out the strategy that you wish not to use.
 	  
      #to_explore = ex_strategy_one(num_iterations)
      #to_explore = ex_strategy_two(num_total_iterations)
      to_explore = ex_strategy_three(g, num_games)
      
      action = 0 
      
      if to_explore:
     	#explore
        #print "explore\n"
        a = random.randint(0, len(actions)-1)
        
        action = actions[a]
      #  print "action {}".format(action)
      else:
        # exploit
        num_iterations += 1
        #print "exploit\n"
        action = lookup_max_a(Q,s, actions)
        #print "action {}".format(action)
        #action = a # actions[a]


      # Get result of throw from dart thrower; update score if necessary
      loc = throw.throw(action) 
      #print "score {}".format(s)
      #print "throw value:{}".format(throw.location_to_score(loc))
      #should reward be based on action of loc?
      reward = darts.R(s,action) 
      #print "reward {}".format(reward)
      s_prime = s - throw.location_to_score(loc)
      if s_prime < 0:
        s_prime = s
                
      # now we update the q score table
      #oldQ = copy.deepcopy(Q[s][a])
      oldQ = (Q[s][action])
      #print "oldQ {}".format(oldQ)
      nextQaction = lookup_max_a(Q, s_prime, actions)
      #print "nextQaction {}".format(nextQaction)
      newQ = oldQ + alpha*(reward + gamma*(Q[s_prime][nextQaction]) - oldQ)
      #print "newQ {}".format(newQ)
      Q[s][action] = newQ
      #print "Q[s][a] {}".format(Q[s][a])
      #print "in game {},score {}, throw value {}, oldQ {}, newQ{}".format(g,s,throw.location_to_score(loc),oldQ,newQ)

      s = s_prime
    #print gamethrows
  print "Average turns = ", float(num_iterations)/float(num_games/2)
  #print "Average turns = ", float(num_total_iterations)/float(num_games)

