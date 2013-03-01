# Renzo Lucioni (HUID: 90760092)
# Daniel Broudy (HUID: 30797418)

from neural_net import NeuralNetwork, NetworkFramework
from neural_net import Node, Target, Input
import random


# <--- Problem 3, Question 1 --->

def FeedForward(network, input):
  """
  Arguments:
  ---------
  network : a NeuralNetwork instance
  input   : an Input instance

  Returns:
  --------
  Nothing

  Description:
  -----------
  This function propagates the inputs through the network. That is,
  it modifies the *raw_value* and *transformed_value* attributes of the
  nodes in the network, starting from the input nodes.

  Notes:
  -----
  The *input* arguments is an instance of Input, and contains just one
  attribute, *values*, which is a list of pixel values. The list is the
  same length as the number of input nodes in the network.

  i.e: len(input.values) == len(network.inputs)

  This is a distributed input encoding (see lecture notes 7 for more
  informations on encoding)

  In particular, you should initialize the input nodes using these input
  values:

  network.inputs[i].raw_value = input[i]
  """
  network.CheckComplete()
  # 1) Assign input values to input nodesi
  for i in range(len(network.inputs)):
      network.inputs[i].raw_value = input.values[i]
      network.inputs[i].transformed_value = NeuralNetwork.Sigmoid(network.inputs[i].raw_value) 

  # 2) Propagates to hidden layer
  for node in network.hidden_nodes:
      node.raw_value = NeuralNetwork.ComputeRawValue(node)
      node.transformed_value = NeuralNetwork.Sigmoid(node.raw_value) 

  # 3) Propagates to the output layer
  for node in network.outputs:
      node.raw_value = NeuralNetwork.ComputeRawValue(node)
      node.transformed_value = NeuralNetwork.Sigmoid(node.raw_value) 

#< --- Problem 3, Question 2

def Backprop(network, input, target, learning_rate):
  """
  Arguments:
  ---------
  network       : a NeuralNetwork instance
  input         : an Input instance
  target        : a target instance
  learning_rate : the learning rate (a float)

  Returns:
  -------
  Nothing

  Description:
  -----------
  The function first propagates the inputs through the network
  using the Feedforward function, then backtracks and update the
  weights.

  Notes:
  ------
  The remarks made for *FeedForward* hold here too.

  The *target* argument is an instance of the class *Target* and
  has one attribute, *values*, which has the same length as the
  number of output nodes in the network.

  i.e: len(target.values) == len(network.outputs)

  In the distributed output encoding scenario, the target.values
  list has 10 elements.

  When computing the error of the output node, you should consider
  that for each output node, the target (that is, the true output)
  is target[i], and the predicted output is network.outputs[i].transformed_value.
  In particular, the error should be a function of:

  target[i] - network.outputs[i].transformed_value
  
  """
  network.CheckComplete()
  # 1) We first propagate the input through the network
  FeedForward(network,input)
  # 2) Then we compute the errors and update the weigths starting with the last layer
  # 3) We now propagate the errors to the hidden layer, and update the weights there too
  
  # Update the err and delta for each output node
  for i in range(len(network.outputs)):
      node = network.outputs[i]
      node.err = target[i] - node.transformed_value
      node.delta = node.err * NeuralNetwork.SigmoidPrime(node.transformed_value) 

  # Update the err and delta for each hidden_node
  # Below loop indexes from the high to low.
  num = len(network.hidden_nodes)
  for i in range(num-1, -1, -1):
      node = network.hidden_nodes[i]
      node.err = 0
      for j in range(len(node.forward_neighbors)):
          node.err += node.forward_weights[j].value * node.forward_neighbors[j].delta
      node.delta = node.err * NeuralNetwork.SigmoidPrime(node.transformed_value)

  # Update the weights fo the outputs 
  for i in range(len(network.outputs)):
      node = network.outputs[i]
      for j in range(len(node.weights)):
          node.weights[j].value += (learning_rate * node.inputs[j].transformed_value * node.delta)

  # Update the weights fo the hidden_nodes 
  for i in range(len(network.hidden_nodes)):
      node = network.hidden_nodes[i]
      for j in range(len(node.weights)):
          node.weights[j].value += (learning_rate * node.inputs[j].transformed_value * node.delta)

  #for i in range(len(network.outputs)):
  #    node = network.outputs[i]
  #    err = target[i] - node.transformed_value
  #    node.delta = err * NeuralNetwork.SigmoidPrime(node.transformed_value) 
  #    for j in range(len(node.weights)):
  #        node.weights[j] = node.weights[j] + (learning_rate * node.inputs[j].transformed_value * node.delta)        

  #num = len(network.hidden_nodes)
  #this will loop backwards from last node in hidden nodes
  #for i in range(num-1,-1,-1):
  #    node = network.hidden_nodes[i]
  #    error = 0
  #    for j in range(len(node.forward_neighbors)):
  #        error = error + node.forward_neighbors[j].weight * node.forward_neighbors[j].delta
  #    node.delta = NeuralNetwork.SigmoidPrime(node.transformed_value) * error
  #    for k in range(len(node.inputs)):
  #        node.weight[k] = node.weight[k] + (learning_rate * node.inputs[k].transformed_value * node.delta)

# <--- Problem 3, Question 3 --->

def Train(network, inputs, targets, learning_rate, epochs):
  """
  Arguments:
  ---------
  network       : a NeuralNetwork instance
  inputs        : a list of Input instances
  targets       : a list of Target instances
  learning_rate : a learning_rate (a float)
  epochs        : a number of epochs (an integer)

  Returns:
  -------
  Nothing

  Description:
  -----------
  This function should train the network for a given number of epochs. That is,
  run the *Backprop* over the training set *epochs*-times
  """
  network.CheckComplete()
#def Backprop(network, input, target, learning_rate):
  for i in range(epochs):
      for j in range(len(inputs)):
          Backprop(network, inputs[j], targets[j], learning_rate)      

# <--- Problem 3, Question 4 --->

class EncodedNetworkFramework(NetworkFramework):
  def __init__(self):
    """
    Initializatio.
    YOU DO NOT NEED TO MODIFY THIS __init__ method
    """
    super(EncodedNetworkFramework, self).__init__() # < Don't remove this line >
    
  # <--- Fill in the methods below --->

  def EncodeLabel(self, label):
    """
    Arguments:
    ---------
    label: a number between 0 and 9

    Returns:
    ---------
    a list of length 10 representing the distributed
    encoding of the output.

    Description:
    -----------
    Computes the distributed encoding of a given label.

    Example:
    -------
    0 => [1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
    3 => [0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]

    Notes:
    ----
    Make sure that the elements of the encoding are floats.
    
    """
    lst = [0.0] * 10
    lst[label] = 1.0
    return lst

  def GetNetworkLabel(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    the 'best matching' label corresponding to the current output encoding

    Description:
    -----------
    The function looks for the transformed_value of each output, then decides 
    which label to attribute to this list of outputs. The idea is to 'line up'
    the outputs, and consider that the label is the index of the output with the
    highest *transformed_value* attribute

    Example:
    -------

    # Imagine that we have:
    map(lambda node: node.transformed_value, self.network.outputs) => [0.2, 0.1, 0.01, 0.7, 0.23, 0.31, 0, 0, 0, 0.1, 0]

    # Then the returned value (i.e, the label) should be the index of the item 0.7,
    # which is 3
    
    """
    # should get us a list of transformed values we can work with
    #output = map(lambda node: node.transformed_value, self.network.outputs)
    output = [0.0] * len(self.network.outputs)
    for i in range(len(self.network.outputs)):
        output[i] = self.network.outputs[i].transformed_value
    # return the index of the largest object 
    return output.index(max(output))

  def Convert(self, image):
    """
    Arguments:
    ---------
    image: an Image instance

    Returns:
    -------
    an instance of Input

    Description:
    -----------
    The *image* arguments has 2 attributes: *label* which indicates
    the digit represented by the image, and *pixels* a matrix 14 x 14
    represented by a list (first list is the first row, second list the
    second row, ... ), containing numbers whose values are comprised
    between 0 and 256.0. The function transforms this into a unique list
    of 14 x 14 items, with normalized values (that is, the maximum possible
    value should be 1).
    
    """
    def norm_sublst(sublst):
        lst = []
        # loop over 14 because pixels is a 14x14 matrix
        for i in range(14):
            for j in range(14):
                lst.append(sublst[i][j]/256.0)
        return lst
   
    i = Input()
    i.values = norm_sublst(image.pixels)
    return i

  def InitializeWeights(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes the weights with random values between [-0.01, 0.01].

    Hint:
    -----
    Consider the *random* module. You may use the the *weights* attribute
    of self.network.
    
    """
    for weight in self.network.weights:
        weight.value = random.uniform(-0.01,0.01)


#<--- Problem 3, Question 6 --->

class SimpleNetwork(EncodedNetworkFramework):
  def __init__(self):
    """
    Arguments:
    ---------
    Nothing

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a simple network, with 196 input nodes,
    10 output nodes, and NO hidden nodes. Each input node
    should be connected to every output node.
    """
    super(SimpleNetwork, self).__init__() # < Don't remove this line >
    
    net = self.network

    # 1) Adds an input node for each pixel.    
    for i in range(196):
        net.AddNode(Node(), net.INPUT)
    
    # 2) Add an output node for each possible digit label.
    for i in range(10):
        n = Node()
        # print "adding to output\n"
        net.AddNode(n, net.OUTPUT)
        for k in range(196):
            n.AddInput(net.inputs[k], 0.0, net)

#<---- Problem 3, Question 7 --->

class HiddenNetwork(EncodedNetworkFramework):
  def __init__(self, number_of_hidden_nodes=15):
  #def __init__(self, number_of_hidden_nodes=30):
    """
    Arguments:
    ---------
    number_of_hidden_nodes : the number of hidden nodes to create (an integer)

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a network with a hidden layer. The network
    should have 196 input nodes, the specified number of
    hidden nodes, and 10 output nodes. The network should be,
    again, fully connected. That is, each input node is connected
    to every hidden node, and each hidden_node is connected to
    every output node.
    """
    super(HiddenNetwork, self).__init__() # < Don't remove this line >

    net = self.network

    # 1) Adds an input node for each pixel
    
    # 1) Adds an input node for each pixel.    
    for i in range(196):
        net.AddNode(Node(), net.INPUT)
    
    # 2) Adds the hidden layer
    for i in range(number_of_hidden_nodes):
        n = Node()
        net.AddNode(n, net.HIDDEN)
        for k in range(196):
            n.AddInput(net.inputs[k], 0.0, net)


    # 3) Adds an output node for each possible digit label.
    for i in range(10):
        n = Node()
        net.AddNode(n, net.OUTPUT)
        for k in range(number_of_hidden_nodes):
            n.AddInput(net.hidden_nodes[k], 0.0, net)

#<--- Problem 3, Question 8 ---> 

class CustomNetwork(EncodedNetworkFramework):
  def __init__(self, number_of_h1_nodes=30, number_of_h2_nodes=15):
    """
    Arguments:
    ---------
    number_of_h1_nodes : the number of hidden nodes in the first layer
    number_of_h2_nodes : the number of hidden nodes in the second layer

    Returns:
    -------
    Nothing

    Description:
    -----------
    Initializes a network with two hidden layers. The network
    should have 196 input nodes, the specified number of
    hidden nodes, and 10 output nodes. The network should be,
    again, fully connected. That is, each input node is connected
    to every hidden1 node each hidden1 node connected to each hidden2
    and each hidden2 node is connected to
    every output node.
    """
    super(CustomNetwork, self).__init__() # <Don't remove this line>
    
    net = self.network

    # Create the Input nodes
    for i in range(196):
        net.AddNode(Node(), net.INPUT)
    
    h1_nodes = []
    # 2) Adds the first hidden layer
    for i in range(number_of_h1_nodes):
        n = Node()
        net.AddNode(n, net.HIDDEN)
        h1_nodes.append(n)
        for k in range(196):
            n.AddInput(net.inputs[k], 0.0, net)

    h2_nodes = []
    # 3) Adds the second hidden layer
    for i in range(number_of_h2_nodes):
        n = Node()
        net.AddNode(n, net.HIDDEN)
        h2_nodes.append(n)
        for k in range(number_of_h1_nodes):
            n.AddInput(h1_nodes[k], 0.0, net)


    # 3) Adds an output node for each possible digit label.
    for i in range(10):
        n = Node()
        net.AddNode(n, net.OUTPUT)
        for k in range(number_of_h2_nodes):
            n.AddInput(h2_nodes[k], 0.0, net)

