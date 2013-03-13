# clust.py
# -------
# YOUR NAME HERE

import sys
import random
import math
import utils

DATAFILE = "adults.txt"

#validateInput()

def validateInput():
    if len(sys.argv) != 3:
        return False
    if sys.argv[1] <= 0:
        return False
    if sys.argv[2] <= 0:
        return False
    return True


#-----------


def parseInput(datafile):
    """
    params datafile: a file object, as obtained from function `open`
    returns: a list of lists

    example (typical use):
    fin = open('myfile.txt')
    data = parseInput(fin)
    fin.close()
    """
    data = []
    for line in datafile:
        instance = line.split(",")
        instance = instance[:-1]
        data.append(map(lambda x:float(x),instance))
    return data


def printOutput(data, numExamples):
    for instance in data[:numExamples]:
        print ','.join([str(x) for x in instance])


def kmeans(data,k):
    # threshold used to determine when to stop
    threshold = 0.01

    # for each k, set prototype u_k to a random vector in data
    prototypes = random.sample(data,k)
    responsibilities = []
    for d in data:
        responsibilities.append([0]*k)

    while(True):
        # update responsibilities 
        for i in range(len(data)):
            # zero out the responsibility vector
            for s in responsibilities[i]:
                s = 0
            # calculate closest_prototype
            distances = []
            for p in prototypes:
                distances.append(utils.squareDistance(data[i],p))
            responsibilities[i][distances.index(min(distances))] = 1
        
        # update prototypes
        largest_shift = 0.0
        for p in range(len(prototypes)):
            temp = [0.0]*len(prototypes[p])
            point_count = 0
            for j in range(len(responsibilities)):
                if responsibilities[j][p] == 1:
                    temp = [a+b for a,b in zip(temp,data[j])]
                    point_count += 1
            temp = map(lambda x: x/point_count, temp)
            diffs = [math.fabs(a-b) for a,b in zip(prototypes[p],temp)]
            largest_shift = max(diffs)
            prototypes[p] = temp
        
        if largest_shift < threshold:
            break
    
    sq_err = 0.0
    count = 0
    for d in range(len(data)):
        for j in range(len(responsibilities[d])):
            if responsibilities[d][j] == 1:
                sq_err += utils.squareDistance(data[d],prototypes[p])
                count += 1
                break

    mse = sq_err/count

    print "\nMSE: {}".format(mse)
    
    print "\n***CLUSTER MEANS***\n"
    for p in range(len(prototypes)):
        print "CLUSTER {}: {}\n".format(p+1,prototypes[p])



# main
# ----
# The main program loop
# You should modify this function to run your experiments

def main():
    # Validate the inputs
    if(validateInput() == False):
        print "Usage: clust numClusters numExamples"
        sys.exit(1);

    numClusters = int(sys.argv[1])
    numExamples = int(sys.argv[2])

    #Initialize the random seed
    
    random.seed()

    #Initialize the data
    
    dataset = file(DATAFILE, "r")
    if dataset == None:
        print "Unable to open data file"

    data = parseInput(dataset)
    
    dataset.close()
    #printOutput(data,numExamples)

    # ==================== #
    # WRITE YOUR CODE HERE #
    # ==================== #
    
    kmeans(data,numClusters)


if __name__ == "__main__":
    validateInput()
    main()
