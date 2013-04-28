import game_interface
import random
import time

def get_move(view):
  # Choose a random direction.
  # If there is a plant in this location, then try and eat it.
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
  # Choose a random direction
  f = open("images.txt", "a+")
  f.write(str(view.GetLife())+'\n')
  if hasPlant:
    for i in xrange(5):
      #print view.GetImage()
      f = open("images.txt", "a+")
      f.write(str(view.GetImage())+'\n')
  f.close()

  time.sleep(0.1)
  return (random.randint(0, 4), hasPlant)