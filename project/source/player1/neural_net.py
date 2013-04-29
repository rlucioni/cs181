import math
from data_reader import *

class Weight:
  def __init__(self, value):
    self.value = value

class Node:
  """
  Attributes:
  ----------
  inputs            : a list of node who are inputs for this node
  weights           : a list of weight objects, for links with input nodes
  fixed_weight      : w0 in the lecture notes and slides
  forward_neighbors : a list of nodes who are output for this node
  raw_value         : the linear combination of weights and input signals, that is w'x
  transformed_value : the signal emitted by this node, that is g(w'x)

  Description:
  ------------
  The situation can be summarized as follow:


              weights[i]        forward_weights[i]
  inputs[i]   -----------> self ------------------> forward_neighbors[i]

  AND:

  inputs                 \
                           => raw_value => transformed value => 
  weights & fixed_weight /
  

  """
  def __init__(self):
    self.inputs = []
    self.weights = []
    self.fixed_weight = None
    self.forward_neighbors = []
    self.forward_weights = []
    self.raw_value = 0
    self.transformed_value = 0

  def AddInput(self, node, weight, network):
    self.inputs.append(node)
    if not weight:
      weight = network.GetNewWeight()
    self.weights.append(weight)
    node.forward_neighbors.append(self)
    node.forward_weights.append(weight)
    if not self.fixed_weight:
      self.fixed_weight = network.GetNewWeight()

class Input:
  def __init__(self):
    self.values = []

class Target:
  def __init__(self):
    self.values = []


class NeuralNetwork:
  INPUT = 1
  HIDDEN = 2
  OUTPUT = 3

  def __init__(self):
    self.complete = False
    self.inputs = []
    self.hidden_nodes = []
    self.outputs = []
    self.node_set = {}
    self.weights = []

  def GetNewWeight(self):
    weight = Weight(0.0)
    self.weights.append(weight)
    return weight

  def AddNode(self, node, node_type):
    self.CheckIncomplete()
    if node_type == self.INPUT:
      assert len(node.inputs) == 0, 'Input node cannot have inputs'
    # Check that we only reference inputs already in the network
    for input in node.inputs:
      assert input in self.node_set, 'Cannot reference input that is not already in the network'
    self.node_set[node] = True
    if node_type == self.INPUT:
      self.inputs.append(node)
    elif node_type == self.HIDDEN:
      self.hidden_nodes.append(node)
    else:
      assert node_type == self.OUTPUT, 'Unexpected node_type: ' % node_type
      self.outputs.append(node)
    
  def MarkAsComplete(self):
    seen_nodes = {}
    for input in self.inputs:
      seen_nodes[input] = True
      assert len(input.inputs) == 0, 'Inputs should not have inputs of their own.'
    for node in self.hidden_nodes:
      seen_nodes[node] = True
      for input in node.inputs:
        assert input in seen_nodes, ('Node refers to input that was added to the network later than'
          'it.')
    for node in self.outputs:
      assert len(node.forward_neighbors) == 0, 'Output node cannot have forward neighbors.'
      for input in node.inputs:
        assert input in seen_nodes, ('Node refers to input that was added to the network later than'
          'it.')
    self.complete = True

  def CheckComplete(self):
    if self.complete:
      return
    self.MarkAsComplete()

  def CheckIncomplete(self):
    assert not self.complete, ('Tried to modify the network when it has already been marked as'
      'complete')

  @staticmethod
  def ComputeRawValue(node):
    total_weight = 0

    for i in range(len(node.inputs)):
      total_weight += node.weights[i].value * node.inputs[i].transformed_value
    total_weight += node.fixed_weight.value
    return total_weight
  
  @staticmethod
  def Sigmoid(value):
    try:
      return 1.0 / (1 + math.exp(-value))
    except:
      if value < 0:
        return 0.0
      else:
        return 1.0

  @staticmethod
  def SigmoidPrime(value):
    try:
      return math.exp(-value) / math.pow(1 + math.exp(-value), 2)
    except:
      return 0

  def InitFromWeights(self, weights):
    assert len(self.weights) == len(weights), (
      'Trying to initialize from a different sized weight vector.')
    for i in range(len(weights)):
      self.weights[i].value = weights[i]


class NetworkFramework(object):
  def __init__(self):
    self.network = NeuralNetwork()

    # Don't worry about these functions, you 
    # will be asked to implement them in another
    # file. You should not modify them here
    self.FeedForwardFn = None
    self.TrainFn = None


  def EncodeLabel(self, label):
    raise NotImplementedError("This function has not been implemented")

  def GetNetworkLabel(self, label):
    raise NotImplementedError("This function has not been implemented")

  def Convert(self, image):
    raise NotImplementedError("This function has not been implemented")

  def InitializeWeights(self):
    for weight in self.network.weights:
      weight.value = 0

  def DumpSimpleWeights(self):
    DataReader.DumpWeights(self.network.weights, "player1/simple_weights.txt")

  def PopulateSimpleWeights(self):
    #assert(len(self.network.weights) == 0)
    #self.network.weights = DataReader.ReadWeights("simple_weights.txt")
    DataReader.ReadWeights(self.network.weights, "player1/simple_weights.txt")

  def Classify(self, image):
    input = self.Convert(image)
    self.FeedForwardFn(self.network, input)
    return self.GetNetworkLabel()

  def Performance(self, images):

    # Loop over the set of images and count the number correct.
    correct = 0
    for image in images:
      if self.Classify(image) == image.label:
        correct += 1
    return correct * 1.0 / len(images)

  #def Train(self, images, validation_images, test_images, learning_rate, epochs):
  def Train(self, images, validation_images, test_images, learning_rate, max_epochs):

    # Convert the images and labels into a format the network can understand.
    inputs = []
    targets = []
    for image in images:
      inputs.append(self.Convert(image))
      targets.append(self.EncodeLabel(image.label))

    # Initializes performance log
    performance_log = []
    performance_log.append((self.Performance(images), self.Performance(validation_images)))
    
    max_perf_validate = 0.0
    timer = 0

    # Loop through the specified number of training epochs.
    #for i in range(epochs):
    for i in range(max_epochs):
      if i == max_epochs: # or timer == 5:
        self.DumpSimpleWeights()
        return(performance_log)

      # This calls your function in neural_net_impl.py.
      self.TrainFn(self.network, inputs, targets, learning_rate, 1)

      # Print out the current training, validation, and test performance.
      perf_train = self.Performance(images)
      perf_validate = self.Performance(validation_images)
      perf_test = self.Performance(test_images)
      # we're actually printing error at the moment, not performance
      #print '%d Performance: %.8f %.3f %.3f' % (
      print '%d Error: %.8f %.3f %.3f' % (
        i + 1, 1-perf_train, 1-perf_validate, 1-perf_test)

      # updates log
      performance_log.append((perf_train, perf_validate))
      
      # compare perf_validate to max_perf_validate
      if perf_validate > max_perf_validate:
          max_perf_validate = perf_validate
          timer = 0
      else:
          timer += 1

      # also check if we've dropped too low
      if max_perf_validate - perf_validate > 0.5:
          self.DumpSimpleWeights()
          return(performance_log)
    
    self.DumpSimpleWeights()
    return(performance_log)

  def RegisterFeedForwardFunction(self, fn):
    self.FeedForwardFn = fn

  def RegisterTrainFunction(self, fn):
    self.TrainFn = fn
