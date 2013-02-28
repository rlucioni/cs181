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
  # 1) Assign input values to input nodes
  for i in range(len(network.inputs)):
      network.inputs[i].raw_value = input[i]
      network.inputs[i].transformed_value = NeuralNetwork.Sigmoid(network.inputs[i].raw_value) 

  # 2) Propagates to hidden layer
  for node in network.hidden_nodes:
      node.raw_value = NeuralNetwork.ComputeRawValue(node)
      node.transformed_value = NeuralNetwork.Sigmoid(node.raw_value) 

  # i think the below is the same as the above loop.
  #for j in range(len(network.hidden_nodes)):
  #    network.hidden_nodes[j].raw_value = NeuralNetwork.ComputeRawValue(network.hidden_nodes[j])
  #    network.hidden_nodes[j].transformed_value = NeuralNetwork.Sigmoid(network.hidden_nodes[j].raw_value) 
  
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
  for i in range(len(network.outputs)):
      node = network.outputs[i]
      err = target[i] - node.transformed_value
      node.delta = err * NeuralNetwork.SigmoidPrime(node.transformed_value) 
      for j in range(len(node.weights)):
          # update node weight for each hidden_node.
          # lecture6-notes page 7     w_mj <- w_mj + alpha * a_m * delta_j
          # I THINK SOMETHING IS WRONG WITH THIS.
          # do we need to save the old weight? node.old_weights[j] = copy.deep(node.weights[j])
          node.weights[j] = node.weights[j] + (learning_rate * node.inputs[j].transformed_value * node.delta)

  # 3) We now propagate the errors to the hidden layer, and update the weights there too
  num = len(network.hidden_nodes)
  #this will loop backwards from last node in hidden nodes
  # range(from, to, increment) eg.  range (9,-1,-1) = [ 9,8,7,6,5,4,3,2,1,0 ] because zero indexed we to go -1
  for i in range(num-1,-1,-1):
#looping through hidden nodes:
      node = network.hidden_nodes[i]
      error = 0
      for j in range(len(node.forward_neighbors)):
          error = error + node.forward_neighbors[j].weight * node.forward_neighbors[j].delta
      node.delta = NeuralNetwork.SigmoidPrime(node.transformed_value) * error
      for k in range(len(node.inputs)):
          node.weight[k] = node.weight[k] + (learning_rate * node.inputs[k].transformed_value * node.delta)

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
    return list

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
    output = map(lambda node: node.transformed_value, self.network.outputs)
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
        new_sublst = []
        # loop over 14 because pixels is a 14x14 matrix
        for i in range(14):
            new_sublst.append(sublst[i]/256.0)
        return new_sublst

    return map(norm_sublst, image.pixels)

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
    
    # 1) Adds an input node for each pixel.    
    # 2) Add an output node for each possible digit label.
    pass


#<---- Problem 3, Question 7 --->

class HiddenNetwork(EncodedNetworkFramework):
  def __init__(self, number_of_hidden_nodes=15):
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

    # 1) Adds an input node for each pixel
    # 2) Adds the hidden layer
    # 3) Adds an output node for each possible digit label.
    pass
    

#<--- Problem 3, Question 8 ---> 

class CustomNetwork(EncodedNetworkFramework):
  def __init__(self):
    """
    Arguments:
    ---------
    Your pick.

    Returns:
    --------
    Your pick

    Description:
    -----------
    Surprise me!
    """
    super(CustomNetwork, self).__init__() # <Don't remove this line>
    pass
