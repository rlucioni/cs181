import random
import copy
import os
import math
 
EXPLORE_TURNS = 10000
EPSILON = 5

ALPHA = .3
GAMMA = .5

# obtain this file's parent directory
parent_dir = os.path.dirname(os.path.abspath(__file__))

# list of all possible states: ATE_NUTRITIOUS, ATE_POISONOUS, SEEN_NOTHING, PASSED
def get_states():
#  states = range(4)
  states = range(20);
  return states
# distance from origin
# if distance >= 20 state = 20  

# Returns a list of all possible actions
# These are the directions (numbers defined in problem)
def get_actions():
  actions = range(4)  
  return actions
#0 = move towards origin
#1 = move clockwise
#2 = move counterclockwise
#3 = move away from origin.

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


def lookup_max_a(Q_table,state):
  cur_val = 0
  action = 0
  actions = get_actions()
  for a in actions:
    curent = Q_table[state][a]
    if curent >= cur_val:
      cur_val = curent
      action = a
  return action

# load the Q table from a file
def load_Q_table():
  f = open(parent_dir+"/q_table.txt", "r")
  
  Q = {}
  states = get_states()
  actions = get_actions()
  # Initialize all the Q values to values from the file!
  for s in states:
    Q[s]= {}
    for a in actions:
        Q[s][a] = float(f.readline())
  Q_table = Q
  f.close()
  return Q_table

def writeout_Q_table(Q_table):
  states = get_states()
  actions = get_actions()
  f = open(parent_dir+"/q_table.txt", "w")
  for s in states:
    for a in actions:
        f.write(str(Q_table[s][a])+'\n')
  f.flush()
  f.close()


# get our next move
def Q_get_move(Q_table, s):
  #to_explore = ex_strategy_one(num_iterations)
  #to_explore = ex_strategy_two(num_total_iterations)
  #to_explore = ex_strategy_three(g, num_games)
  to_explore = 0
  states = get_states()
  actions = get_actions()

  action = 0 
  
  if to_explore:
    a = random.randint(0, 3)
    action = actions[a]
  else:
    action = lookup_max_a(Q_table,s)
    #action = a # actions[a]
  return action

def R(cur_state, changeinhealth):
    if changeinhealth > 0:
        reward = changeinhealth
    else:
        reward = 0;
    if cur_state >=19:
        reward = -10
    return reward
    

# The Q-learning algorithm:
def Q_learning(Q_table, prev_state, prev_action, cur_state, changeinhealth):
      states = get_states()
      actions = get_actions()
      #reward = changeinhealth #R(s,action) 
      reward = R(cur_state, changeinhealth)
      s_prime = cur_state
      s = prev_state
      a = prev_action

      # now we update the q score table
      oldQ = (Q_table[s][a])
      nextQaction = lookup_max_a(Q_table, s_prime)
      newQ = oldQ + ALPHA*(reward + GAMMA*(Q_table[s_prime][nextQaction]) - oldQ)
      Q_table[s][a] = newQ



# HELPER FUNCTIONS
def pos_to_state(x,y):
    dist = math.sqrt(x*x + y*y)
    a = int(round(dist,0))
    if a >= 20:
      # all distances greater than 19 are bundled into state 19
      return 19
    else:
      return a
    #return int(round(dist,0))
