
class Image:
  def __init__(self, label):
    self.pixels = []
    self.label = label

class DataReader:
  @staticmethod
  def GetImages(filename, limit):
    """Returns a list of image objects
    filename: The file to read in
    limit: The maximum number of images to read.  -1 = no limit
    """
    images = []
    infile = open(filename, 'r')
    ct = 0
    cur_row = 0
    image = None
    while True:
      line = infile.readline().strip()
      if not line:
        break
      if line.find('#') == 0:
        if image:
          images.append(image)
          ct += 1
          if ct > limit and limit != -1:
            break
        image = Image(int(line[1:]))
      else:
        line2 = line[1:-1]
        image.pixels.append([float(r) for r in line2.strip().split(", ")])
    if image:
      images.append(image)
    return images

  @staticmethod
  def ConvertTuple(tup):
    string = str(tup)
    stripped = string[1:-1]
    image = Image(-1)
    image.pixels.append([float(r) for r in stripped.strip().split(", ")])
    return image

  @staticmethod
  def DumpWeights(weights, filename):
    """Dump the weights vector to filename"""
    outfile = open(filename, 'w')
    for weight in weights:
      outfile.write('%r\n' % weight.value)

  @staticmethod
  def ReadWeights(weights, filename):
    """Returns a weight vector retrieved by reading file filename"""
    infile = open(filename, 'r')
    weight_values = []
    for line in infile:
      weight = float(line.strip())
      weight_values.append(weight)
    assert( len(weight_values) == len(weights))
    for i in range(len(weights)):
      weights[i].value = weight_values[i]
    #return weights
