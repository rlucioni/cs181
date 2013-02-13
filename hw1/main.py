# main.py
# -------
# Renzo Lucioni (HUID: 90760092)
# Daniel Broudy (HUID: 30797418)

from dtree import *
import sys

class Globals:
    noisyFlag = False
    pruneFlag = False
    valSetSize = 0
    dataset = None


##Classify
#---------

def classify(decisionTree, example):
    return decisionTree.predict(example)

##Learn
#------
def learn(dataset):
    learner = DecisionTreeLearner()
    learner.train(dataset)
    return learner.dt

##Validate
#---------
def validate(decisionTree, val_fold,sz):
    "Return the  number correctly scored  by a decision tree"
    correct = 0
    for j in range(sz):
        if classify(decisionTree, val_fold[j]) == val_fold[j].attrs[-1]:
            correct += 1
        return correct

##Score
#------
def score(decisionTree, train_folds, train_size, test_fold):
    train_correct = validate(decisionTree, train_folds, train_size)
    test_correct = validate(decisionTree, test_fold, 10)
    return train_correct, test_correct

##Prune
#------
def prune(decisionTree, val_fold):
    #iterate over branches! (just like display method)
    decisionTree.display()

    print "################################"
    
    #RENZOOO:: 
    # this sucessfully creates a new leaf node that classifies 1
    # and places it instead of what was classified by 10 
    # if you look at the bottom of the two printed trees you will see.
    node = DecisionTree(1,classification=1)
    decisionTree.replace(10,node);
    decisionTree.display()    
    #print decisionTree.branches
#    if decisionTree.nodetype == DecisionTree.LEAF:
#        return
#    for (val, subtree) in decisionTree.branches.items():
#        if isinstance(subtree, DecisionTree):
#            subtree.prune(subtree, val_fold)
#        else:

# main
# ----
# The main program loop
# You should modify this function to run your experiments

def parseArgs(args):
  """Parses arguments vector, looking for switches of the form -key {optional value}.
  For example:
    parseArgs([ 'main.py', '-n', '-p', 5 ]) = { '-n':True, '-p':5 }"""
  args_map = {}
  curkey = None
  for i in xrange(1, len(args)):
    if args[i][0] == '-':
      args_map[args[i]] = True
      curkey = args[i]
    else:
      assert curkey
      args_map[curkey] = args[i]
      curkey = None
  return args_map

def validateInput(args):
    args_map = parseArgs(args)
    valSetSize = 0
    noisyFlag = False
    pruneFlag = False
    boostRounds = -1
    maxDepth = -1
    if '-n' in args_map:
      noisyFlag = True
    if '-p' in args_map:
      pruneFlag = True
      valSetSize = int(args_map['-p'])
    if '-d' in args_map:
      maxDepth = int(args_map['-d'])
    if '-b' in args_map:
      boostRounds = int(args_map['-b'])
    return [noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds]

def main():
    arguments = validateInput(sys.argv)
    noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds = arguments
    print noisyFlag, pruneFlag, valSetSize, maxDepth, boostRounds

    # Read in the data file
    
    if noisyFlag:
        f = open("noisy.csv")
    else:
        f = open("data.csv")

    data = parse_csv(f.read(), " ")
    dataset = DataSet(data)
    
    # Copy the dataset so we have two copies of it
    examples = dataset.examples[:]
 
    dataset.examples.extend(examples)
    dataset.max_depth = maxDepth
    if boostRounds != -1:
      dataset.use_boosting = True
      dataset.num_rounds = boostRounds

    # ====================================
    # WRITE CODE FOR YOUR EXPERIMENTS HERE
    # ====================================
    
    train_accuracy, test_accuracy = 0, 0

    if pruneFlag:
        for i in range(1): #REMEMBER TO MAKE THIS 10 AGAIN!!!
            test_fold = dataset.examples[10*i:10*(i+1)]
            train_folds = dataset.examples[10*(i+1):10*(i+1)+(90-valSetSize)]
            val_fold = dataset.examples[10*(i+1)+(90-valSetSize):10*(i+1)+90]
            # fix for breaking on the 54th data point 
            train_set = DataSet(train_folds, values=dataset.values)
        
            # learn
            learner = DecisionTreeLearner()
            learner.train(train_set)
            tree = learner.dt
            # call these two instead so we can have a DecisionTreeLearner    
            #tree = learn(train_set)
            #tree_cor = validate(tree, val_fold, valSetSize)

            # prune
            # print "PRUNE {}".format(i)
            prune(tree, val_fold)

            # testing
            train_score, test_score = score(tree, train_folds, 90-valSetSize, test_fold)

            train_accuracy += train_score/90.0
            test_accuracy += test_score/10.0
        
        print "CROSS-VALIDATED TRAINING PERFORMANCE: {}".format(train_accuracy/10.0)
        print "CROSS-VALIDATED TEST PERFORMANCE: {}".format(test_accuracy/10.0)
    
    else:
        for i in range(10):
            test_fold = dataset.examples[10*i:10*(i+1)]
            train_folds = dataset.examples[10*(i+1):10*(i+1)+90]
            # fix for breaking on the 54th data point 
            train_set = DataSet(train_folds, values=dataset.values)
        
            # learn
            tree = learn(train_set)
        
            # testing
            train_score, test_score = score(tree, train_folds, 90, test_fold)

            train_accuracy += train_score/90.0
            test_accuracy += test_score/10.0

        print "CROSS-VALIDATED TRAINING PERFORMANCE: {}".format(train_accuracy/10.0)
        print "CROSS-VALIDATED TEST PERFORMANCE: {}".format(test_accuracy/10.0)
main()

def compareTrees(dt1, dt2):
    """function for comparing two decision trees, the function calls 
      score on the test set."""
    return 0

#
# I need to write a function that takes a decision tree and a validation set
# this function will for each node from the bottom up try to replace the node 
# with the most common value below it instead and see which does better on the
# validation set. 
# to find out you have a LEAF or NODE you use self.nodetype.
# if it is a LEAF if has a self.classification
# 
def prunetree(self, dtLearner):
    return 0    








