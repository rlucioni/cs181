import common
import game_interface
import random
import time
from data_reader import *
from __init__ import *

#def get_move(view):
#  #return common.get_move(view)
#  return common.get_move(view,"images1.txt","value1.txt")

def get_move(view):
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT 
  eat = -1
  if hasPlant:
    nutritious_count = 0
    while (eat == -1):
      unprocessed_image = view.GetImage()
      image = DataReader.ConvertTuple(unprocessed_image)
      if network.Classify(image):
        nutritious_count += 1
      else:
        nutritious_count -= 1

      if nutritious_count == 1:
        eat = 1
      elif nutritious_count == -1:
        eat = 0

  time.sleep(0.1)
  return (random.randint(0, 4), eat)
  #return (1, eat)
