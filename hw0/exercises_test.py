# Import the math module, so that we have access to the functions sqrt and pow
import unittest
import math
from exercises import *

class TestExercises(unittest.TestCase):
  def setUp(self):
    pass

  def test_factorial(self):
    self.assertEqual(1, factorial(0))
    self.assertEqual(6, factorial(3))

  def test_sumFile(self):
    total = sumFile('test_sum_file.txt')
    self.assertEqual(48.2, total, 0.01)

  def test_point(self):
    point = Point(1, 2)
    self.assertEqual(math.sqrt(5), point.distanceFromOrigin(), 0.01)

if __name__ == '__main__':
  unittest.main()
