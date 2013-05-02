import math
import unittest
import game_interface

class GameInterfaceTest(unittest.TestCase):
  PLANT_BONUS = 20
  PLANT_PENALTY = 19
  OBSERVATION_COST = 2
  STARTING_LIFE = 10
  LIFE_PER_TURN = 3

  def testGameInterface(self):
    game = game_interface.GameInterface(self.PLANT_BONUS, self.PLANT_PENALTY,
             self.OBSERVATION_COST, self.STARTING_LIFE, self.LIFE_PER_TURN)
    game.StartGame()
    view1 = game.GetPlayer1View()
    view2 = game.GetPlayer2View()
    self.assertEquals(0, view1.GetRound())
    self.assertEquals(0, view1.GetXPos())
    self.assertEquals(0, view1.GetYPos())
    self.assertEquals(0, view2.GetRound())
    self.assertEquals(0, view2.GetXPos())
    self.assertEquals(0, view2.GetYPos())
    for i in xrange(100):
      # Try to observe the plant
      hasPlant = False
      start1 = view1.GetLife()
      start2 = view2.GetLife()
      round1 = view1.GetRound()
      round2 = view2.GetRound()
      self.assertEquals(round1, round2)
      (x1, y1) = (view1.GetXPos(), view1.GetYPos())
      (x2, y2) = (view2.GetXPos(), view2.GetYPos())
      if view1.GetPlantInfo() == game_interface.STATUS_UNKNOWN_PLANT:
        image = view1.GetImage()
        self.assertEquals(start1 - self.OBSERVATION_COST, view1.GetLife())
        start1 -= self.OBSERVATION_COST
        self.assertEquals(36, len(image))
        hasPlant = True
      game.ExecuteMoves(game_interface.UP, hasPlant, game_interface.DOWN, False)
      remaining1 = start1 - self.LIFE_PER_TURN
      life1 = view1.GetLife()
      if hasPlant:
        self.assertTrue((remaining1 + self.PLANT_BONUS) == life1 or 
                        (remaining1 - self.PLANT_PENALTY) == life1)
      else:
        self.assertEquals(remaining1, life1)
      self.assertEquals(start2 - self.LIFE_PER_TURN, view2.GetLife())
      self.assertEquals(round1 + 1, view1.GetRound())
      # Make sure each robot moved one square.
      (new_x1, new_y1) = (view1.GetXPos(), view1.GetYPos())
      (new_x2, new_y2) = (view2.GetXPos(), view2.GetYPos())
      self.assertEquals(1, abs(x1 - new_x1) + abs(y1 - new_y1))
      self.assertEquals(1, abs(x2 - new_x2) + abs(y2 - new_y2))
    # On average, the second robot should be further down than the first robot.
    self.assertTrue(view1.GetYPos() > view2.GetYPos())

if __name__ == '__main__':
  unittest.main()
