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
def validate(decisionTree, fold):
    "Return the  number correctly scored  by a decision tree"
    correct = 0
    for j in range(len(fold)):
        if classify(decisionTree, fold[j]) == fold[j].attrs[-1]:
            correct += 1
    return correct

##Score
#------
def score(decisionTree, train_folds, test_fold):
    train_correct = validate(decisionTree, train_folds)
    test_correct = validate(decisionTree, test_fold)
    return train_correct, test_correct


##Sift
#------
def sift(attr, val, val_fold):
    def f(example):
        return example.attrs[attr] == val
    return filter(f, val_fold)
    
    
##Majority
#---------
def majority(examples):
    yes, no = 0, 0
    for i in range(len(examples)):
        target = examples[i].attrs[-1]
        if target:
            yes += 1
        else:
            no += 1
    print "yes: {}, no: {}\n".format(yes, no)
    if yes > no:
        return 1
    else:
        return 0


##Prune
#------
def prune(decisionTree, val_fold, train_fold):
    # iterate over branches! (just like display method)
    if len(val_fold) == 0:
        return decisionTree
    if decisionTree.nodetype == DecisionTree.LEAF:
        return decisionTree
    if decisionTree.nodetype == DecisionTree.NODE:
        for (val, subtree) in decisionTree.branches.items():
            if isinstance(subtree, DecisionTree):
                #print "val_fold: {}\n".format(val_fold)
                new_val_fold = sift(decisionTree.attrname, val, val_fold)
                #print "new_val_fold: {}\n".format(new_val_fold)
                new_train_fold = sift(decisionTree.attrname, val, train_fold)
                
                decisionTree.replace(val, prune(subtree, new_val_fold, new_train_fold))
        
        leaf = DecisionTree(DecisionTree.LEAF,classification=majority(train_fold))
        
        prune_score = validate(leaf, new_val_fold)
        no_prune_score = validate(decisionTree, new_val_fold)
        
        #print "prune_score = {}, no_prune_score = {}\n".format(prune_score, no_prune_score)

        if prune_score >= no_prune_score:
            #print "returning leaf\n"
            return leaf
        else:
            #print "returning decision tree\n"
            return decisionTree
    

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
            learner = DecisionTreeLearner()
            learner.train(train_set)
            tree = learner.dt

            tree.display()

            print "==========================================="

            new_tree = prune(tree, val_fold, train_folds)
            new_tree.display()

            print "==========================================="
            
            # testing
            train_score, test_score = score(new_tree, train_folds, test_fold)

            train_accuracy += train_score/float(len(train_folds))
            test_accuracy += test_score/10.0
        
        print "CROSS-VALIDATED TRAINING PERFORMANCE (PRUNED): {}".format(train_accuracy/10.0)
        print "CROSS-VALIDATED TEST PERFORMANCE (PRUNED): {}".format(test_accuracy/10.0)
    
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


