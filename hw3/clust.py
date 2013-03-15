# clust.py
# -------
# Renzo Lucioni (HUID: 90760092)
# Daniel Broudy (HUID: 30797418)

import sys
import random
import math
import utils

DATAFILE = "adults.txt"
SMALL_DATAFILE = "adults-small.txt"

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
            for s in range(len(responsibilities[i])):
                responsibilities[i][s] = 0
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
        # will be 3 for the adults-small.txt data
        num_attr = len(clusters[c][0])
        aggregate = [0.0]*num_attr
        for cluster in clusters[c]:
            aggregate = map(sum,zip(aggregate,cluster))
        # numbers of examples in cluster
        n = len(clusters[c])
        means = map(lambda x: x/n, aggregate)
        print "CLUSTER {}: {}\n".format(c+1,means)

    # print "\n***CLUSTERS***\n"
    # for c in range(len(clusters)):
    #     print "CLUSTER {}: {}".format(c+1, clusters[c])
    
    print "\n***NO. EXAMPLES PER CLUSTER***\n"
    for c in range(len(clusters)):
        print "CLUSTER {}: {}\n".format(c+1,len(clusters[c]))

def autoclass(data,k):
    # threshold used to determine when to stop - TF Andrew Mao suggested anywhere between 1e-5 and 1e-10
    threshold = 0.000001
    high = -sys.maxint

    # find means for all attributes
    # should be 48
    num_attr = len(data[0])
    aggregate = [0.0]*num_attr
    for example in data:
        aggregate = map(sum,zip(aggregate,example))
    n = len(data)
    # means for all attributes - we'll use these as cutoffs
    means = map(lambda x: x/n, aggregate)

    # now we process the data to make all attribute values binary
    for example in data:
        for i in range(len(example)):
            if example[i] >= means[i]:
                example[i] = 1
            else:
                example[i] = 0

    responsibilities = []
    for d in data:
        responsibilities.append([0]*k)

    # intialize all theta_k (starting parameters)
    thetas = []
    for j in range(k):
        temp = []
        # theta_kc
        temp.append(1/float(k))
        #for j in range(len(data[0]))
        for d in range(num_attr):
            # theta_d^j
            temp.append(random.random())
        thetas.append(temp)

    clusters = []

    count = 0
    while(True):
        count += 1
        print "ITERATION {}".format(count)
        # expectation
        E_N = [0]*k
        E_D = [[0]*k]*num_attr
        for m in range(len(data)):
            for s in range(len(responsibilities[m])):
                responsibilities[m][s] = 0
            
            ps = []
            for j in range(k):
                prod = 1.0
                for i in range(num_attr):
                    subprod = (thetas[j][i+1]**data[m][i])*(1-thetas[j][i+1])**(1-data[m][i])
                    prod *= subprod
                ps.append(thetas[j][0]*prod)
            
            responsibilities[m][ps.index(max(ps))] = 1
            
            gammas = []
            for p in ps:
                gammas.append(p/float(sum(ps)))

            E_N = [a+b for a,b in zip(E_N,gammas)]

            for a in range(num_attr):
                if data[m][a] == 1:
                    E_D[a] = [x+y for x,y in zip(E_D[a],gammas)]

        # maximization
        for j in range(k):
            thetas[j][0] = E_N[j]/n
            for d in range(num_attr):
                thetas[j][d+1] = E_D[d][j]/E_N[j]

        clusters = []
        for i in range(k):
            clusters.append([])

        for d in range(len(data)):
            for j in range(len(responsibilities[d])):
                if responsibilities[d][j] == 1:
                    clusters[j].append(data[d])
                    break

        log_likelihood = 0.0
        # clusters
        for c in range(len(clusters)):
            running_sum = 0.0
            # examples
            for i in range(len(clusters[c])):
                # attributes
                running_sum += math.log(thetas[c][0])
                for j in range(len(clusters[c][i])):
                    if thetas[c][j+1] > 0 and thetas[c][j+1] < 1:
                        running_sum += (clusters[c][i][j]*math.log(thetas[c][j+1])) + ((1-clusters[c][i][j])*math.log(1.0-(thetas[c][j+1])))
            log_likelihood += running_sum
        print log_likelihood

        if log_likelihood > high + threshold:
            high = log_likelihood
        else:
            break

    print "\n***CLUSTER MEANS***\n"
    for c in range(len(clusters)):
        aggregate = [0.0]*num_attr
        for example in clusters[c]:
            aggregate = map(sum,zip(aggregate,example))
        # numbers of examples in cluster
        n = len(clusters[c])
        if n == 0:
            means = map(lambda x: x*0, aggregate)
        else:
            means = map(lambda x: x/n, aggregate)
        print "CLUSTER {}: {}\n".format(c+1,means)




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

    
    #Initialize the full dataset for K-means
    
    dataset = file(DATAFILE, "r")
    if dataset == None:
        print "Unable to open data file"

    full_data = parseInput(dataset)
    
    dataset.close()
    #printOutput(data,numExamples)

    data = random.sample(full_data,numExamples)

    # print "\nK-MEANS:"
    # kmeans(data,numClusters)

    autoclass(data,numClusters)
    
    
    #Initialize the small dataset for HAC
    
    # dataset = file(SMALL_DATAFILE, "r")
    # if dataset == None:
    #     print "Unable to open data file"

    # full_data = parseInput(dataset)
    
    # dataset.close()
    # #printOutput(data,numExamples)
    
    # data = random.sample(full_data,numExamples)
    
    # print "\nHAC, MIN:"
    # hac(data,numClusters,utils.cmin)

    # print "\nHAC, MAX:"
    # hac(data,numClusters,utils.cmax)

    # print "\nHAC, MEAN:"
    # hac(data,numClusters,utils.cmean)
    
    # print "\nHAC, CENTROID:"
    # hac(data,numClusters,utils.ccent)


if __name__ == "__main__":
    validateInput()
    main()
