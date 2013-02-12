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

##Score
#------
def score(decisionTree, train_folds, test_fold):
    train_correct, test_correct = 0, 0
    # calculating training score (9 of 10 folds = 90 data points)
    for j in range(90):
        if classify(decisionTree, train_folds[j]) == train_folds[j].attrs[-1]:
            train_correct += 1
    # calculating test score (1 fold = 10 data points)
    for k in range(10):
        if classify(decisionTree, test_fold[k]) == test_fold[k].attrs[-1]:
            test_correct += 1
    return train_correct, test_correct

##Prune
#------
#def prune(decisionTree, val_fold):
    # implement

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
        for i in range(10):
            test_fold = dataset.examples[10*i:10*(i+1)]
            train_folds = dataset.examples[10*(i+1):10*(i+1)+(90-valSetSize)]
            val_fold = dataset.examples[10*(i+1)+(90-valSetSize):10*(i+1)+90]
            # fix for breaking on the 54th data point 
            train_set = DataSet(train_folds, values=dataset.values)
        
            # learn
            tree = learn(train_set)
            
            # prune
            prune(tree, val_fold)

            # testing
            train_score, test_score = score(tree, train_folds, test_fold)

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
            train_score, test_score = score(tree, train_folds, test_fold)

            train_accuracy += train_score/90.0
            test_accuracy += test_score/10.0

        print "CROSS-VALIDATED TRAINING PERFORMANCE: {}".format(train_accuracy/10.0)
        print "CROSS-VALIDATED TEST PERFORMANCE: {}".format(test_accuracy/10.0)
main()
