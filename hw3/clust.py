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
                sq_err += utils.squareDistance(data[d],prototypes[j])
                count += 1
                break

    mse = sq_err/count

    print "\nMSE: {}".format(mse)
    
    print "\n***CLUSTER MEANS***\n"
    for p in range(len(prototypes)):
        print "CLUSTER {}: {}\n".format(p+1,prototypes[p])


def hac(data, k, metric):
    # make each example a singleton cluster
    clusters = []
    for example in data:
        clusters.append([example])
    
    N = len(data)
    for iteration in range(N-k):
        C = len(clusters)
        a_index = None
        b_index = None
        min_dist = sys.maxint
        for i in range(C-1):
            for j in range(i+1,C):
                dist = metric(clusters[i],clusters[j],utils.squareDistance)
                if dist < min_dist:
                    min_dist = dist
                    a_index = i
                    b_index = j
        # pop this one first to preserve the index we're popping below
        # otherwise could be out of range, or wrong, so we pop after 
        # it in the list
        B = clusters.pop(b_index)
        A = clusters.pop(a_index)
        clusters.append(A+B)

    print "\n***CLUSTER MEANS***\n"
    for c in range(len(clusters)):
        n = len(clusters[c])
        aggregate = [0.0]*n
        for cluster in clusters[c]:
            aggregate = map(sum,zip(aggregate,cluster))
        means = map(lambda x: x/n, aggregate)
        print "CLUSTER {}: {}\n".format(c+1,means)
    
    print "\n***NO. EXAMPLES PER CLUSTER***\n"
    for c in range(len(clusters)):
        print "CLUSTER {}: {}\n".format(c+1,len(clusters[c]))

    # record distances between all pairs of examples 
    # flat upper triangular matrix
    #distances = []
    #for i in range(len(clusters)):
    #    distances.append([])
    #    for j in range(i+1,len(data)):
    #        distances[i].append(metric(clusters[i],clusters[j],squareDistance))

    #N = len(data)
    #for iteration in range(N-k):
        # find a and b, the two 'closest' clusters
    #    min_dists = []
    #    for cluster in clusters:
    #        min_dists.append(min(cluster))
    #    shortest = min(min_dists)
    #    min_index = min_dists.index(shortest)
    #    for l in range(len(clusters[min_index])):
    #        if clusters[min_index][l] == shortest:
                # set to infinity, retain list structure
    #            clusters[min_index][l] = sys.maxint



# main
# ----
# The main program loop
# You should modify this function to run your experiments

def main():
    # Validate the inputs
    if(validateInput() == False):
        print "Usage: clust.py numClusters numExamples"
        sys.exit(1);

    numClusters = int(sys.argv[1])
    numExamples = int(sys.argv[2])

    #Initialize the random seed
    
    random.seed()

    #Initialize the data
    
    dataset = file(DATAFILE, "r")
    if dataset == None:
        print "Unable to open data file"

    full_data = parseInput(dataset)
    
    dataset.close()
    #printOutput(data,numExamples)

    data = random.sample(full_data,numExamples)

    print "\nK-MEANS:"
    kmeans(data,numClusters)

    print "\nHAC, MIN:"
    hac(data,numClusters,utils.cmin)

    print "\nHAC, MAX:"
    hac(data,numClusters,utils.cmax)

    print "\nHAC, MEAN:"
    hac(data,numClusters,utils.cmean)
    
    print "\nHAC, CENTROID:"
    hac(data,numClusters,utils.ccent)

if __name__ == "__main__":
    validateInput()
    main()
