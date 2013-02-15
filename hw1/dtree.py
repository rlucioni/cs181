"""Learn to estimate functions from examples. (Chapters 18-20)"""

from utils import *
import random, operator

#______________________________________________________________________________

class Example:
  """A class that holds an example.  An example is a list of attributes along
  with a weight.  The default is for all examples to have the same weight of
  1."""
  def __init__(self, attrs):
    self.attrs = attrs
    self.weight = 1

class DataSet:
    """A data set for a machine learning problem.  It has the following fields:

    d.examples    A list of examples.  Each one is an instance of class Example.
    d.attrs       A list of integers to index into an example, so example[attr]
                  gives a value. Normally the same as range(len(d.examples)). 
    d.attrnames   Optional list of mnemonic names for corresponding attrs.
    d.target      The attribute that a learning algorithm will try to predict.
                  By default the final attribute.
    d.inputs      The list of attrs without the target.
    d.values      A list of lists, each sublist is the set of possible
                  values for the corresponding attribute. If None, it
                  is computed from the known examples by self.setproblem.
                  If not None, an erroneous value raises ValueError.
    d.name        Name of the data set (for output display only).
    d.source      URL or other source where the data came from.
    
    Configuration Parameters
    d.max_depth      The max_depth for decision trees (optional; default=-1)
    d.use_boosting   Whether or not boosting should be used to train.
    d.num_rounds     The number of rounds to use for boosting

    Normally, you call the constructor and you're done; then you just
    access fields like d.examples and d.target and d.inputs."""

    def __init__(self, examples=None, attrs=None, target=-1, values=None,
                 attrnames=None, name='', source='',
                 inputs=None, exclude=(), doc=''):
        """Accepts any of DataSet's fields.  Examples can
        also be a string or file from which to parse examples using parse_csv.
        >>> DataSet(examples='1, 2, 3')
        <DataSet(): 1 examples, 3 attributes>
        """
        update(self, name=name, source=source, values=values)
        # Initialize .examples from string or list or data directory
        if isinstance(examples, str):
            self.examples = parse_csv(examples)
        elif examples is None:
            self.examples = parse_csv(DataFile(name+'.csv').read())
        else:
            self.examples = examples
        # Attrs are the indicies of examples, unless otherwise stated.
        if not attrs and self.examples:
            attrs = range(len(self.examples[0].attrs))
        self.attrs = attrs
        map(self.check_example, self.examples)
        # Initialize .attrnames from string, list, or by default
        if isinstance(attrnames, str): 
            self.attrnames = attrnames.split()
        else:
            self.attrnames = attrnames or attrs
        self.setproblem(target, inputs=inputs, exclude=exclude)
        self.max_depth = -1
        self.use_boosting = False
        self.num_rounds = 0

    def setproblem(self, target, inputs=None, exclude=()):
        """Set (or change) the target and/or inputs.
        This way, one DataSet can be used multiple ways. inputs, if specified,
        is a list of attributes, or specify exclude as a list of attributes
        to not put use in inputs. Attributes can be -n .. n, or an attrname.
        Also computes the list of possible values, if that wasn't done yet."""
        self.target = self.attrnum(target)
        exclude = map(self.attrnum, exclude)
        if inputs:
            self.inputs = removall(self.target, inputs)
        else:
            self.inputs = [a for a in self.attrs
                           if a is not self.target and a not in exclude]
        if not self.values:
            self.values = map(unique, zip(*[e.attrs for e in self.examples]))

    def add_example(self, example):
        """Add an example to the list of examples, checking it first."""
        self.check_example(example)
        self.examples.append(example)

    def check_example(self, example):
        """Raise ValueError if example has any invalid values."""
        if self.values:
            for a in self.attrs:
                if example.attrs[a] not in self.values[a]:
                    raise ValueError('Bad value %s for attribute %s in %s' %
                                     (example.attrs[a], self.attrnames[a], example))

    def attrnum(self, attr):
        "Returns the number used for attr, which can be a name, or -n .. n."
        if attr < 0:
            return len(self.attrs) + attr
        elif isinstance(attr, str): 
            return self.attrnames.index(attr)
        else:
            return attr

    def sanitize(self, example):
       "Return a copy of example, with non-input attributes replaced by 0."
       return [i in self.inputs and example.attrs[i] for i in range(len(example.attrs))] 

    def __repr__(self):
        return '<DataSet(%s): %d examples, %d attributes>' % (
            self.name, len(self.examples), len(self.attrs))

#______________________________________________________________________________

def parse_csv(input, delim=','):
    r"""Input is a string consisting of lines, each line has comma-delimited 
    fields.  Convert this into a list of lists.  Blank lines are skipped.
    Fields that look like numbers are converted to numbers.
    The delim defaults to ',' but '\t' and None are also reasonable values.
    >>> parse_csv('1, 2, 3 \n 0, 2, na')
    [[1, 2, 3], [0, 2, 'na']]
    """
    lines = [line for line in input.splitlines() if line.strip() is not '']
    list_of_lists = [map(num_or_str, line.split(delim)) for line in lines]
    examples = []
    for attrs in list_of_lists:
      examples.append(Example(attrs))
    return examples

def rms_error(predictions, targets):
    return math.sqrt(ms_error(predictions, targets))

def ms_error(predictions, targets):
    return mean([(p - t)**2 for p, t in zip(predictions, targets)])

def mean_error(predictions, targets):
    return mean([abs(p - t) for p, t in zip(predictions, targets)])

def mean_boolean_error(predictions, targets):
    return mean([(p != t)   for p, t in zip(predictions, targets)])


#______________________________________________________________________________

class Learner:
    """A Learner, or Learning Algorithm, can be trained with a dataset,
    and then asked to predict the target attribute of an example."""

    def train(self, dataset): 
        self.dataset = dataset

    def predict(self, example): 
        # overridden by class DecisionTreeLearner
        abstract

#______________________________________________________________________________

class MajorityLearner(Learner):
    """A very dumb algorithm: always pick the result that was most popular
    in the training data.  Makes a baseline for comparison."""

    def train(self, dataset):
        "Find the target value that appears most often."
        self.most_popular = mode([e[dataset.target] for e in dataset.examples])

    def predict(self, example):
        "Always return same result: the most popular from the training set."
        return self.most_popular

#______________________________________________________________________________

class NaiveBayesLearner(Learner):
    
    def train(self, dataset):
        """Just count the target/attr/val occurences.
        Count how many times each value of each attribute occurs.
        Store count in N[targetvalue][attr][val]. Let N[attr][None] be the
        sum over all vals."""
        N = {}
        ## Initialize to 0
        for gv in self.dataset.values[self.dataset.target]:
            N[gv] = {}
            for attr in self.dataset.attrs:
                N[gv][attr] = {}
                for val in self.dataset.values[attr]:
                    N[gv][attr][val] = 0
                    N[gv][attr][None] = 0
        ## Go thru examples
        for example in self.dataset.examples:
            Ngv = N[example[self.dataset.target]]
            for attr in self.dataset.attrs:
                Ngv[attr][example[attr]] += 1
                Ngv[attr][None] += 1
        self._N = N

    def N(self, targetval, attr, attrval):
       "Return the count in the training data of this combination."
       try:
          return self._N[targetval][attr][attrval]
       except KeyError:
          return 0

    def P(self, targetval, attr, attrval):
        """Smooth the raw counts to give a probability estimate.
        Estimate adds 1 to numerator and len(possible vals) to denominator."""
        return ((self.N(targetval, attr, attrval) + 1.0) /
                (self.N(targetval, attr, None) + len(self.dataset.values[attr])))

    def predict(self, example):
        """Predict the target value for example. Consider each possible value,
        choose the most likely, by looking at each attribute independently."""
        possible_values = self.dataset.values[self.dataset.target]
        def class_probability(targetval):
            return product([self.P(targetval, a, example[a])
                            for a in self.dataset.inputs], 1)
        return argmax(possible_values, class_probability)

#______________________________________________________________________________

class NearestNeighborLearner(Learner):

    def __init__(self, k=1):
        "k-NearestNeighbor: the k nearest neighbors vote."
        self.k = k

    def predict(self, example):
        """With k=1, find the point closest to example.
        With k>1, find k closest, and have them vote for the best."""
        if self.k == 1:
            neighbor = argmin(self.dataset.examples,
                              lambda e: self.distance(e, example))
            return neighbor[self.dataset.target]
        else:
            ## Maintain a sorted list of (distance, example) pairs.
            ## For very large k, a PriorityQueue would be better
            best = [] 
            for e in examples:
                d = self.distance(e, example)
                if len(best) < k: 
                    e.append((d, e))
                elif d < best[-1][0]:
                    best[-1] = (d, e)
                    best.sort()
            return mode([e[self.dataset.target] for (d, e) in best])

    def distance(self, e1, e2):
        return mean_boolean_error(e1, e2)

#______________________________________________________________________________

class DecisionTree:
    """A DecisionTree is either a NODE or a LEAF.  A LEAF simply holds a classification.
    A NODE holds an attribute that is being tested, along with a dict of
    {attrval: DecisionTree} entries which gives the child trees for different
    values of attr."""

    NODE, LEAF = range(2)

    def __init__(self, nodetype, attr=None, classification=None, attrname=None, branches=None):
        "Initialize by saying what attribute this node tests."
        self.nodetype = nodetype
        if nodetype == DecisionTree.LEAF:
			    self.classification = classification
        else:
          # Sets self.attr = attr, self.attrname = attrname or attr, etc.
          update(self, attr=attr, attrname=attrname or attr,
                 branches=branches or {})

    def predict(self, example):
        "Given an example, use the tree to classify the example."
        if self.nodetype == DecisionTree.LEAF:
          return self.classification
        child = self.branches[example.attrs[self.attr]]
        return child.predict(example)

    def add(self, val, subtree):
        "Add a branch.  If self.attr = val, go to the given subtree."
        self.branches[val] = subtree
        return self

    def replace(self, val, subtree):
         "Replace a branch. Used in constructing pruned versions of trees"
         del self.branches[val]
         self.branches[val] = subtree
         return self

    def display(self, indent=0):
        if self.nodetype == DecisionTree.LEAF:
            print "leaf %d" % self.classification
            return
        name = self.attrname
        print 'Test', name
        for (val, subtree) in self.branches.items():
            print ' '*4*indent, name, '=', val, '==>',
            if isinstance(subtree, DecisionTree):
                subtree.display(indent+1)
            else:
                print 'RESULT = ', subtree

    def __repr__(self):
        if self.nodetype == DecisionTree.LEAF:
            return 'Leaf(%r)' % self.classification
        return 'DecisionTree(%r, %r, %r)' % (
            self.attr, self.attrname, self.branches)

Yes, No = True, False
        
#______________________________________________________________________________

class DecisionTreeLearner(Learner):

    def predict(self, example):
        return self.dt.predict(example)

    def train(self, dataset):
        self.dataset = dataset
        self.attrnames = dataset.attrnames
        self.dt = self.decision_tree_learning(dataset.examples, dataset.inputs)

    def decision_tree_learning(self, examples, attrs, default=None):
        if len(examples) == 0:
            return DecisionTree(DecisionTree.LEAF, classification=default)
        elif self.all_same_class(examples):
            return DecisionTree(DecisionTree.LEAF,
                                classification=examples[0].attrs[self.dataset.target])
        elif  len(attrs) == 0:
            return DecisionTree(DecisionTree.LEAF, classification=self.majority_value(examples))
        else:
            best = self.choose_attribute(attrs, examples)
            tree = DecisionTree(DecisionTree.NODE, attr=best, attrname=self.attrnames[best])
            for (v, examples_i) in self.split_by(best, examples):
                subtree = self.decision_tree_learning(examples_i,
                  removeall(best, attrs), self.majority_value(examples))
                tree.add(v, subtree)
            return tree

    def choose_attribute(self, attrs, examples):
        "Choose the attribute with the highest information gain."
        return argmax(attrs, lambda a: self.information_gain(a, examples))

    def all_same_class(self, examples):
        "Are all these examples in the same target class?"
        target = self.dataset.target
        class0 = examples[0].attrs[target]
        for e in examples:
           if e.attrs[target] != class0: return False
        return True

    def majority_value(self, examples):
        """Return the most popular target value for this set of examples.
        (If target is binary, this is the majority; otherwise plurality.)"""
        g = self.dataset.target
        return argmax(self.dataset.values[g],
                      lambda v: self.count(g, v, examples))

    def count(self, attr, val, examples):
        return count_if(lambda e: e.attrs[attr] == val, examples)
    
    def information_gain(self, attr, examples):
        def I(examples):
            target = self.dataset.target
            return information_content([self.count(target, v, examples)
                                        for v in self.dataset.values[target]])
        N = float(len(examples))
        remainder = 0
        for (v, examples_i) in self.split_by(attr, examples):
            remainder += (len(examples_i) / N) * I(examples_i)
        return I(examples) - remainder

    def split_by(self, attr, examples=None):
        "Return a list of (val, examples) pairs for each val of attr."
        if examples == None:
            examples = self.dataset.examples
        return [(v, [e for e in examples if e.attrs[attr] == v])
                for v in self.dataset.values[attr]]
    
def information_content(values):
    "Number of bits to represent the probability distribution in values."
    # If the values do not sum to 1, normalize them to make them a Prob. Dist.
    values = removeall(0, values)
    s = float(sum(values))
    if s != 1.0: values = [v/s for v in values]
    return sum([- v * log2(v) for v in values])

#______________________________________________________________________________

# should take number of rounds as a parameter?
class AdaBoostLearner(Learner):

    def predict(self, example):
        return self.dt.predict(example)

    def train(self, dataset):
        self.dataset = dataset
        self.attrnames = dataset.attrnames
        self.dt = self.decision_tree_learning(dataset.examples, dataset.inputs)

    def decision_tree_learning(self, examples, attrs, default=None):
        if len(examples) == 0:
            return DecisionTree(DecisionTree.LEAF, classification=default)
        elif self.all_same_class(examples):
            return DecisionTree(DecisionTree.LEAF,
                                classification=examples[0].attrs[self.dataset.target])
        elif  len(attrs) == 0:
            return DecisionTree(DecisionTree.LEAF, classification=self.majority_value(examples))
        else:
            best = self.choose_attribute(attrs, examples)
            tree = DecisionTree(DecisionTree.NODE, attr=best, attrname=self.attrnames[best])
            for (v, examples_i) in self.split_by(best, examples):
                subtree = self.decision_tree_learning(examples_i,
                  removeall(best, attrs), self.majority_value(examples))
                tree.add(v, subtree)
            return tree

    def choose_attribute(self, attrs, examples):
        "Choose the attribute with the highest information gain."
        return argmax(attrs, lambda a: self.information_gain(a, examples))

    def all_same_class(self, examples):
        "Are all these examples in the same target class?"
        target = self.dataset.target
        class0 = examples[0].attrs[target]
        for e in examples:
           if e.attrs[target] != class0: return False
        return True

    # use weighted sum to select majority
    def majority_value(self, examples):
        """Return the most popular target value for this set of examples.
        (If target is binary, this is the majority; otherwise plurality.)"""
        g = self.dataset.target
        return argmax(self.dataset.values[g],
                      lambda v: self.count(g, v, examples))

    # should sum weights - how to deal with labels 1-10?
    def count(self, attr, val, examples):
        return count_if(lambda e: e.attrs[attr] == val, examples)
    
    # work with example weighted sum instead of count
    def information_gain(self, attr, examples):
        def I(examples):
            target = self.dataset.target
            return information_content([self.count(target, v, examples)
                                        for v in self.dataset.values[target]])
        N = float(len(examples))
        remainder = 0
        for (v, examples_i) in self.split_by(attr, examples):
            remainder += (len(examples_i) / N) * I(examples_i)
        return I(examples) - remainder

    def split_by(self, attr, examples=None):
        "Return a list of (val, examples) pairs for each val of attr."
        if examples == None:
            examples = self.dataset.examples
        return [(v, [e for e in examples if e.attrs[attr] == v])
                for v in self.dataset.values[attr]]
    
def information_content(values):
    "Number of bits to represent the probability distribution in values."
    # If the values do not sum to 1, normalize them to make them a Prob. Dist.
    values = removeall(0, values)
    s = float(sum(values))
    if s != 1.0: values = [v/s for v in values]
    return sum([- v * log2(v) for v in values])

