import game_interface
import random
import time

#def get_move(view):
def get_move(view,img_filename,val_filename):
  # Choose a random direction.
  # If there is a plant in this location, then try and eat it.
  
  hasPlant = view.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT
  
  # Choose a random direction
  #f = open(val_filename, "r+")
  # assumes we only have numbers as strings
  #prev_val = int(f.readline())
  
  #cur_val = view.GetLife()
  #.seek(0)
  #f.write(str(cur_val)+'\n')
  #f.flush()
  #f.close()
  
  #g = open(img_filename, "a+")
  #diff = cur_val - prev_val
  # label the previous image
  #if diff == 1:
  #  g.write('#N\n')
  #elif diff == -1:
  #  g.write('#P\n')
  #g.flush()
  #g.close()
 
  if hasPlant:
    #g = open(img_filename, "a+")
    for i in xrange(5):
      print view.GetImage()
      #g.write(str(view.GetImage())+'\n')
      #g.write('('+str(view.GetXPos())+', '+str(view.GetYPos())+')\n')
    #g.flush()
    #g.close()

  #time.sleep(0.1)
  return (random.randint(0, 4), hasPlant)
