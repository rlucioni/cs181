# Import the math module, so that we have access to the functions sqrt and pow
import math

def factorial(x):
  """Return x!, assuming that x is a non-negative integer."""
  if x == 0:
      return 1
  return x*factorial(x-1)

def sumFile(filename):
  """Each line of filename contains a float.  Return the sum of all lines in the
  file."""
  infile = open(filename, 'r')
  sum = 0.0
  for line in infile:
      sum = sum + float(line)
  return sum

# This is the syntax for a Python class.
class Point():
  """Class that encapsulates a single point in the x-y plane."""

  # This is the constructor for the class.  By convention, the first argument to
  # any method of the class is self, referring to the variable itself.  This is
  # similar to the "this" variable in other programming languages.
  def __init__(self, x_coord, y_coord):
    self.x = x_coord
    self.y = y_coord

  def distanceFromOrigin(self):
    return math.sqrt(math.pow(self.x,2) + math.pow(self.y,2))
