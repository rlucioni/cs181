#
# Darts playing model for CS181.
#

import sys
import time
import random
import throw
import mdp
import modelbased
import modelfree

GAMMA = .5
#EPOCH_SIZE = 10


# <CODE HERE>: Complete this function, which should return a
# list of all possible states.
def get_states():
  # should return a **list** of states. Each state should be an integer.
  states = range(throw.START_SCORE+1)
  return states

# Returns a list of all possible actions, or targets, which include both a
# wedge number and a ring.
def get_actions():

  actions = []
  
  for wedge in throw.wedges:
    actions = actions + [throw.location(throw.CENTER, wedge)]
    actions = actions + [throw.location(throw.INNER_RING, wedge)]
    actions = actions + [throw.location(throw.FIRST_PATCH, wedge)]
    actions = actions + [throw.location(throw.MIDDLE_RING, wedge)]
    actions = actions + [throw.location(throw.SECOND_PATCH, wedge)]
    actions = actions + [throw.location(throw.OUTER_RING, wedge)]
    
  return actions

# <CODE HERE>: Define the reward function
def R(s,a):
  # takes a state s and action a
  # returns the reward for completing action a in state s
  points = throw.location_to_score(a)
  if points > s: 
    return 0
  else:
    return points


# Play a single game 
def play(method):
    score = throw.START_SCORE
    turns = 0
    
    if method == "mdp":
        target = mdp.start_game(GAMMA)
    else:
        target = modelfree.start_game()
        
    targets = []
    results = []
    while(True):
        turns = turns + 1
        result = throw.throw(target)
        targets.append(target)
        results.append(result)
        raw_score = throw.location_to_score(result)
        #if raw_score > score:
            # update Q[s][a]
        #else:
            #modelfree.Q_learning(score,target,raw_score)
        print "Target: wedge", target.wedge,", ring", target.ring
        print "Result: wedge", result.wedge,", ring", result.ring
        print "Raw Score:", raw_score
        print "Score:", score
        if raw_score <= score:
            score = int(score - raw_score)
        else:
            print
            print "TOO HIGH!"
        if score == 0:
            break

        if method == "mdp":
            target = mdp.get_target(score)
        else:
            target = modelfree.get_target(score)
            
    print "WOOHOO!  It only took", turns, " turns"
    #end_game(turns)
    return turns

# Play n games and return the average score. 
def test(n, method):
    score = 0
    for i in range(n):
        score += play(method)
        
    print "Average turns = ", float(score)/float(n)
    return score

# <CODE HERE>: Feel free to modify the main function to set up your experiments.
def main(epoch_sz):
    throw.init_board()
    #num_games = 1000
    num_games = 100


#************************************************#
# Uncomment the lines below to run the mdp code, #
# using the simple dart thrower that matches     #
# the thrower specified in question 2.           #
#*************************************************

# Default is to solve MDP and play 1 game
    #throw.use_simple_thrower()
    #test(1, "mdp")    

#*************************************************#
# Uncomment the lines below to run the modelbased #
# code using the complex dart thrower.            #
#*************************************************#

# Seed the random number generator -- the default is
# the current system time. Enter a specific number
# into seed() to keep the dart thrower constant across
# multiple calls to main().
# Then, initialize the throwing model and run
# the modelbased algorithm.
    random.seed(42)
    throw.init_thrower()
    #modelbased.modelbased(GAMMA, EPOCH_SIZE, num_games)
    modelbased.modelbased(GAMMA, epoch_sz, num_games)

#*************************************************#
# Uncomment the lines below to run the modelfree  #
# code using the complex dart thrower.            #
#*************************************************#

# Plays 1 game using a default player. No modelfree
# code is provided. 
    #random.seed()
    #throw.init_thrower()
    #test(1, "modelfree")


if __name__ =="__main__":
    #main()
    #print "### TIME T MODE SWITCHING ###"
    print "### EPSILON-GREEDY ###"
    print "EPOCH SIZE: 3"
    main(3)
    print "EPOCH SIZE: 10"
    main(10)
    print "EPOCH SIZE: 100"
    main(100)




