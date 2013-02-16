# main.py
# -------
# Renzo Lucioni (HUID: 90760092)
# Daniel Broudy (HUID: 30797418)

from dtree import *
from utils import *
import sys

class Globals:
    noisyFlag = False
    pruneFlag = False
    #pruneFlag = True
    valSetSize = 0
    dataset = None


##Classify
#---------
def classify(decisionTree, example):
    return decisionTree.predict(example)

##Democracy
#----------
def democracy(weighted_tree_list, example):
    "Takes a weighted set of decision trees and classifies an instance/example by having the trees vote on the label."
    yea = 0.0
    for i in range(len(weighted_tree_list)):
        if weighted_tree_list[i][0].predict(example):
            yea += weighted_tree_list[i][1]
        else:
            yea -= weighted_tree_list[i][1]
    if yea > 0:
        return 1
    else:
        return 0

##Learn
#------
# takes a DataSet type
def learn(dataset):
    e = 2.71828
    learner = DecisionTreeLearner()
    # AdaBoost wrapper
    if dataset.use_boosting:
        weighted_tree_set = []
        for i in range(dataset.num_rounds):
            # dataset needs to be mutable here
            learner.train(dataset)
            tree = learner.dt
            # calculate WEIGHTED TRAINING ERROR
            error = weighted_error(tree, dataset.examples)
            #print "ERROR = {}".format(error)
            if error == 0.0:
                return [(tree,sys.maxint)]
            else:
                # change of base
                alpha = .5*(log2((1-error)/error) / log2(e))
                #print "ALPHA = {}".format(alpha)
                weight_seq = []
                for j in range(len(dataset.examples)):
                    if classify(tree, dataset.examples[j]) == dataset.examples[j].attrs[-1]:
                        dataset.examples[j].weight *=  e**(-alpha)
                    else:
                        dataset.examples[j].weight *= e**alpha
                    weight_seq.append(dataset.examples[j].weight)
                normalized_seq = normalize(weight_seq)
                for k in range(len(dataset.examples)):
                    dataset.examples[k].weight = normalized_seq[k]
                weighted_tree_set.append((tree,alpha))
        return weighted_tree_set
    else:
        learner.train(dataset)
        return learner.dt

##Weighted Error
#--------------
def weighted_error(tree, examples):
    "Return the weighted error of a tree"
    epsilon = 0.0
    for i in range(len(examples)):
        if classify(tree, examples[i]) != examples[i].attrs[-1]:
            epsilon += examples[i].weight
    return epsilon

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
def score(tree_set, train_folds, test_fold, boost):
    train_correct,test_correct = 0,0
    if boost:
        for i in range(len(train_folds)):
            if democracy(tree_set, train_folds[i]) == train_folds[i].attrs[-1]:
                train_correct += 1
        for j in range(len(test_fold)):
            if democracy(tree_set, test_fold[j]) == test_fold[j].attrs[-1]:
                test_correct += 1
        return train_correct, test_correct
    else:
        train_correct = validate(tree_set, train_folds)
        test_correct = validate(tree_set, test_fold)
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
    yes, no = 0.0, 0.0
    for i in range(len(examples)):
        target = examples[i].attrs[-1]
        if target:
            yes += examples[i].weight
        else:
            no += examples[i].weight
    #print "yes: {}, no: {}\n".format(yes, no)
    if yes > no:
        return 1
    else:
        return 0


##Prune
#------
def prune(decisionTree, val_fold, train_fold):
    # stop if there is nothing left in the validation set
    # SHOULD RETURN LEAF? (since we don't need anything below here...)
    if len(val_fold) == 0:
        return decisionTree
        # return DecisionTree(DecisionTree.LEAF,classification=majority(train_fold))
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
    #if Globals.noisyFlag:
        f = open("noisy.csv")
    else:
        f = open("data.csv")

    data = parse_csv(f.read(), " ")
    dataset = DataSet(data)
    
    # Copy the dataset so we have two copies of it
    examples = dataset.examples[:]
 
    dataset.examples.extend(examples)
    
    #boostRounds = -1
    #maxDepth = -1
    
    dataset.max_depth = maxDepth
    if boostRounds != -1:
      dataset.use_boosting = True
      dataset.num_rounds = boostRounds

    # ====================================
    # WRITE CODE FOR YOUR EXPERIMENTS HERE
    # ====================================
    
    train_accuracy, test_accuracy = 0., 0.
    
    # valSetSize = Globals.valSetSize

    if pruneFlag:
    #if Globals.pruneFlag:
        for i in range(0,100,10):
            test_fold = dataset.examples[i:(i+10)]
            train_folds = dataset.examples[(i+10):(i+100-valSetSize)]
            val_fold = dataset.examples[(i+100-valSetSize):(i+100)]
            # fix for breaking on the 54th data point 
            train_set = DataSet(train_folds, values=dataset.values)
        
            # learn
            tree = learn(train_set)

            #tree.display()

            #print "==========================================="

            new_tree = prune(tree, val_fold, train_folds)
            #new_tree.display()

            #print "==========================================="
            
            # testing
            train_score, test_score = score(new_tree, train_folds, test_fold, 0)

            train_accuracy += train_score/float(len(train_folds))
            test_accuracy += test_score/10.0
        
        # return train_accuracy/10.0, test_accuracy/10.0
        
        print "CROSS-VALIDATED TRAINING PERFORMANCE (PRUNED): {}".format(train_accuracy/10.0)
        print "CROSS-VALIDATED TEST PERFORMANCE (PRUNED): {}".format(test_accuracy/10.0)
    
    elif dataset.use_boosting:
        for i in range(0,100,10):
            test_fold = dataset.examples[i:(i+10)]
            train_folds = dataset.examples[(i+10):(i+100)]
            train_set = DataSet(train_folds, values=dataset.values)
            train_set.max_depth = maxDepth
            if boostRounds != -1:
                train_set.use_boosting = True
                train_set.num_rounds = boostRounds
        
            # learn
            weighted_tree_set = learn(train_set)

            # testing
            train_score, test_score = score(weighted_tree_set, train_folds, test_fold, 1)

            train_accuracy += train_score/90.0
            test_accuracy += test_score/10.0
        
        # return train_accuracy/10.0, test_accuracy/10.0
        
        print "CROSS-VALIDATED TRAINING PERFORMANCE (BOOSTED): {}".format(train_accuracy/10.0)
        print "CROSS-VALIDATED TEST PERFORMANCE (BOOSTED): {}".format(test_accuracy/10.0)
    
    else:
        for i in range(0,100,10):
            test_fold = dataset.examples[i:(i+10)]
            train_folds = dataset.examples[(i+10):(i+100)]
            # fix for breaking on the 54th data point 
            train_set = DataSet(train_folds, values=dataset.values)
        
            # learn
            tree = learn(train_set)
        
            # testing
            train_score, test_score = score(tree, train_folds, test_fold, 0)

            train_accuracy += train_score/90.0
            test_accuracy += test_score/10.0

        print "CROSS-VALIDATED TRAINING PERFORMANCE: {}".format(train_accuracy/10.0)
        print "CROSS-VALIDATED TEST PERFORMANCE: {}".format(test_accuracy/10.0)

main()

#############################################################
#### The code below is for generating the graphs for 2b. ####
#### Other required changes to main.py for this code to  #### 
#### run properly are commented above.                   ####
#############################################################

# import matplotlib.pyplot as plt
# from pylab import *

### NON-NOISY ###
# ys = []
# zs = []

# for i in range(80):
#     Globals.valSetSize = i+1
#     y, z = main()
#     ys.append(y)
#     zs.append(z)

# plt.clf()

# # these must have the same dimension
# # valSetSize
# xs = range(1,81)
# # training accuracy
# #ys = [.3, .5, .1, .8, 1]
# # test accuracy
# #zs = [.6, .4, .0, .07, .9]

# p1, = plt.plot(xs, ys, color='b')
# p2, = plt.plot(xs, zs, color='r')

# plt.title('Performance on Non-Noisy Data')
# # plt.title('Performance on Noisy Data')
# plt.xlabel('Validation Set Size')
# plt.ylabel('Predictive Accuracy')
# plt.axis([0,80,0,1])
# plt.legend((p1,p2,), ('Training Accuracy', 'Test Accuracy',), 'lower right')

# # save figure as a pdf
# savefig('prune-non-noisy.pdf')

### NOISY ###
# ys = []
# zs = []

# Globals.noisyFlag = True
# for i in range(80):
#     Globals.valSetSize = i+1
#     y, z = main()
#     ys.append(y)
#     zs.append(z)

# plt.clf()

# # these must have the same dimension
# # valSetSize
# xs = range(1,81)
# # training accuracy
# #ys = [.3, .5, .1, .8, 1]
# # test accuracy
# #zs = [.6, .4, .0, .07, .9]

# p1, = plt.plot(xs, ys, color='b')
# p2, = plt.plot(xs, zs, color='r')

# plt.title('Performance on Noisy Data')
# # plt.title('Performance on Noisy Data')
# plt.xlabel('Validation Set Size')
# plt.ylabel('Predictive Accuracy')
# plt.axis([0,80,0,1])
# plt.legend((p1,p2,), ('Training Accuracy', 'Test Accuracy',), 'lower right')

# # save figure as a pdf
# savefig('prune-noisy.pdf')






