

# Components of a darts player. #

# 
 # Modify the following functions to produce a player.
 # The default player aims for the maximum score, unless the
 # current score is less than or equal to the number of wedges, in which
 # case it aims for the exact score it needs.  You can use this
 # player as a baseline for comparison.
 #

from random import *
import throw
import darts

# make pi global so computation need only occur once
PI = {}
EPSILON = .001


# actual
def start_game(gamma):

  infiniteValueIteration(gamma)
  for ele in PI:
    print "score: ", ele, "; ring: ", PI[ele].ring, "; wedge: ", PI[ele].wedge
  
  return PI[throw.START_SCORE]

def get_target(score):

  return PI[score]

# define transition matrix/function
def T(a, s, s_prime):
  # takes an action a, current state s, and next state s_prime
  # returns the probability of transitioning to s_prime when taking action a in state s

  p_transition = 0.0
  probabilities = [0.4, 0.2, 0.2, 0.1, 0.1]

  # trick to allow wrap around
  wedge_list = throw.wedges*3

  # calculate all 5 wedges you could end up in when aiming for a.wedge
  wedge_index = len(throw.wedges) + throw.wedges.index(a.wedge)
  candidate_wedges = [wedge_list[wedge_index], wedge_list[wedge_index+1], wedge_list[wedge_index-1], wedge_list[wedge_index+2], wedge_list[wedge_index-2]]

  # calulate all 5 regions/rings (some may be the same) you could end up in when aiming for a.ring, with prob array
  if a.ring == throw.CENTER:
    candidate_rings = [a.ring, throw.INNER_RING, throw.INNER_RING, throw.FIRST_PATCH, throw.FIRST_PATCH]
  elif a.ring == throw.INNER_RING:
    candidate_rings = [a.ring, throw.FIRST_PATCH, throw.CENTER, throw.MIDDLE_RING, throw.INNER_RING]
  else:
    candidate_rings = [a.ring, a.ring+1, a.ring-1, a.ring+2, a.ring-2]

  # for each (ring, wedge) pair, calculate point value, and check if it gets you from s to s_prime
  for w in range(len(candidate_wedges)):
    for r in range(len(candidate_rings)):
      # instantiation of location class
      real_location = throw.location(candidate_rings[r],candidate_wedges[w])
      if s - throw.location_to_score(real_location) == s_prime:
        p_transition += probabilities[r]*probabilities[w]

  return p_transition


def infiniteValueIteration(gamma):
  # takes a discount factor gamma and convergence cutoff epsilon
  # returns

  V = {}
  Q = {}
  V_prime = {}
  
  states = darts.get_states()
  actions = darts.get_actions()

  notConverged = True

  # intialize value of each state to 0
  for s in states:
    V[s] = 0
    Q[s] = {}

  # until convergence is reached
  while notConverged:

    # store values from previous iteration
    for s in states:
      V_prime[s] = V[s]

    # update Q, pi, and V
    for s in states:
      for a in actions:

        # given current state and action, sum product of T and V over all states
        summand = 0
        for s_prime in states:
          summand += T(a, s, s_prime)*V_prime[s_prime]

        # update Q
        Q[s][a] = darts.R(s, a) + gamma*summand

      # given current state, store the action that maximizes V in pi and the corresponding value in V
      PI[s] = actions[0]
      V[s] = Q[s][PI[s]]
      for a in actions:
        if V[s] <= Q[s][a]:
          V[s] = Q[s][a]
          PI[s] = a

    notConverged = False
    for s in states:
      if abs(V[s] - V_prime[s]) > EPSILON:
        notConverged = True
        
  
