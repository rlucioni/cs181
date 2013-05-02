#from random import *
import random
import copy
 
EXPLORE_TURNS = 10000
EPSILON = 5

ALPHA = .5
GAMMA = .3

# list of all possible states.
def get_states():
  states = range(4)
  return states
#state 1: see nothing
#state 2: eaten Nut
#state 3: eaten Pois
#state 4: eaten Passed


# Returns a list of all possible actions, or targets, which include both a
def get_actions():
  
  actions = range(4)  
  return actions
  #these are the directions (numbers defined in problem.)

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
  actions = get.actions()
  for a in actions:
    curent = Q_table[state][a]
    if curent >= cur_val:
      cur_val = curent
      action = a
  return action

# load the Q table from a file
def Load_Q_table():
  # FILENAME WILL BE: q_table.txt
  f = open("q_table.txt", "r")
  
  Q = {}
  states = get_states()
  actions = get_actions()
  # Initialize all the Q values to values from the file!
  for s in states:
    Q[s]= {}
    for a in actions:
        Q[s][a] = float(f.readline())#WHATDOESITEQUAL!

  Q_table = Q
  f.close()
  return Q_table

def Writeout_Q_table(Q_table):
  #FILENAME WILL BE: q_table.txt
  states = get_states()
  actions = get_actions()
  f = open("q_table.txt", "r+")
  #f.seek(0)
  for s in states:
    for a in actions:
        f.write(str(Q_table[s][a])+'\n')
  f.flush()
  f.close()


# get our next move
def Q_get_move(Q_table):
  #to_explore = ex_strategy_one(num_iterations)
  #to_explore = ex_strategy_two(num_total_iterations)
  #to_explore = ex_strategy_three(g, num_games)
  to_explore = 1
  states = get_states()
  actions = get_actions()

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
    action = lookup_max_a(Q_table,s)
    #print "action {}".format(action)
    #action = a # actions[a]

  return a


# The Q-learning algorithm:
def Q_learn_it(Q_table, prev_state, prev_action, cur_state, changeinhealth):
      states = get_states()
      actions = get_actions()
      reward = changeinhealth #R(s,action) 
      s_prime = cur_state
      s = prev_state
      a = prev_action

      # now we update the q score table
      oldQ = (Q_table[s][a])
      #print "oldQ {}".format(oldQ)
      nextQaction = lookup_max_a(Q_table, s_prime)
      #print "nextQaction {}".format(nextQaction)
      newQ = oldQ + ALPHA*(reward + GAMMA*(Q_table[s_prime][nextQaction]) - oldQ)
      #print "newQ {}".format(newQ)
      Q_table[s][a] = newQ
      #print "Q[s][a] {}".format(Q[s][a])
      #print "in game {},score {}, throw value {}, oldQ {}, newQ{}".format(g,s,throw.location_to_score(loc),oldQ,newQ)


