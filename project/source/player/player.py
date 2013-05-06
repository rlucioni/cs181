import game_interface
import random
import time
import copy
import modelfree
import math
from data_reader import *
from __init__ import *

#ATE_NUTRITIOUS = 0
#ATE_POISONOUS = 1
#SEEN_NOTHING = 2
#PASSED = 3

def get_move(view):
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT

  cur_life = view.GetLife()
  
  if hasattr(view, 'previous_life'):
    diff = cur_life - view.previous_life
    view.previous_life = cur_life
  else:
    diff = 0

  x, y = view.GetXPos(), view.GetYPos()
  cur_state = modelfree.pos_to_state(x,y)
#  cur_state = 0
#  if hasattr(view, 'old_hasPlant'):
#    if view.old_hasPlant == 0:
#      cur_state = SEEN_NOTHING
#    elif view.ate == 0:
#      cur_state = PASSED
#    elif diff < 0:
#      cur_state = ATE_POISONOUS
#    elif diff > 1:
#      cur_state = ATE_NUTRITIOUS
#  else:
#    cur_state = PASSED

#  view.old_hasPlant = hasPlant

  if hasattr(view, 'prev_state'):
    modelfree.Q_learning(q_table, view.prev_state, view.prev_action, cur_state, diff)

  eat = -1
  if hasPlant:
    nutritious_count = 0
    while (eat == -1):
      unprocessed_image = view.GetImage()
      image = DataReader.ConvertTuple(unprocessed_image)
      # FINITE MEMORY POLICY (K=2)
      if network.Classify(image):
        #nutritious_count += 1
        if nutritious_count == 1:
          eat = 1
        else:
          nutritious_count = 1
      else:
        #nutritious_count -= 1
        if nutritious_count == -1:
          eat = 0
        else:
          nutritious_count = -1

      # for FINITE STATE CONTROLLER
      #if nutritious_count == 2:
      #  eat = 1
      #elif nutritious_count == -2:
      #  eat = 0

  view.ate = eat
  view.prev_state = cur_state
  view.prev_action = modelfree.Q_get_move(q_table,cur_state)
  xy_action = circ_action_to_lrud(x,y,view.prev_action)
  # process action to a left-right-up-down from circular actions 
  

  #modelfree.writeout_Q_table(q_table)
  #time.sleep(0.1)
  
  # MOVEMENT 
  # 0: up, 1: left, 2: down, 3: right
  
  # Q-LEARNED MOVEMENT
  return (view.prev_action, eat)
  return (xy_action, eat)

  # SEMI-RANDOM MOVEMENT
#  x, y = view.GetXPos(), view.GetYPos()
#  # when outside of circle centered at the origin with radius 20, move back to the origin, otherwise move randomly
#  dist_from_origin = math.sqrt(x**2 + y**2)
#  if dist_from_origin > 20:
#    #move to origin
#    if abs(x) > abs(y):
#      if x >= 0:
#        return (1, eat)
#      else:
#        return (3, eat)
#    else:
#      if y >= 0:
#        return (2, eat)
#      else:
#        return (0, eat)
#  else:
#    return (random.randint(0, 3), eat)  

  # RANDOM MOVEMENT
  #return (random.randint(0, 3), eat)

def xy_action_to_opposite(action):
    if action == 0:
        return 2
    if action == 1:
        return 3
    if action == 2:
        return 0
    if action == 3:
         return 1

def circ_action_to_lrud(x,y,action):
  if action == 0 | action == 1:
    return internal_circ_action_to_lrud(x,y,action)
  else:
    a = internal_circ_action_to_lrud(x,y,action)
    return xy_action_to_opposite(a)
        

  # MOVEMENT 
  # 0: up, 1: left, 2: down, 3: right
  # CIRCULAR MOVEMENT
  # 0: in, 1: cw, 2: ccw, 3: out
def internal_circ_action_to_lrud(x,y,action):
  x_mag = int(math.fabs(x))
  y_mag = int(math.fabs(y))    
  greater = 0;
  if x_mag > y_mag:
      greater = x
  else:
      greater = y
  
  if action == 0: # move to origin
    if greater > 0:
      #move to decrease greater
      if greater == x:
        # move left
        return 1
      else: #y value is positive and greater
        return 2
        #move down
    else:
      if greater == x:
        return 3
        #move right
      else:
        return 0
        #move up
  if action == 1: # move to clock
    if greater == y:
      if y > 0:
        #move right
        return 3
      else:
        #move left
        return 1
    else: 
      if x > 0:
        #move down
        return 2
      else:
        return 0
        #move up
       
