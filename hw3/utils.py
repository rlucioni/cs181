import itertools

def argmin(seq, fn):
    """Return an element with lowest fn(seq[i]) score; tie goes to first one.
    >>> argmin(['one', 'to', 'three'], len)
    'to'
    """
    best = seq[0]; best_score = fn(best)
    for x in seq:
        x_score = fn(x)
        if x_score < best_score:
            best, best_score = x, x_score
    return best


def squareDistance(xs, ys):
    """ Computes the square distance of two vectors in n dimensions
    >>> squareDistance([1,2,3], [2,3,4])
    """
    res = sum( [(x - y)**2 for x,y in zip(xs,ys)] )
    return(res)

def cmin(c1, c2, d):
    """ computes the min distance between two clusters `c1` and `c2`, using
    `d` as a reference measure
    example:
    c1 = [ [1,2], [2,3] ]
    c2 = [ [2,3], [6,7] ]
    ccent(c1, c2, squareDistance)
    """
    min_dist = d(c1[0], c2[0])
    for x in c1:
        for y in c2:
            tmp_dist = d(x,y)
            if tmp_dist < min_dist:
                min_dist = tmp_dist
    return(min_dist)


def cmax(c1, c2, d):
    """ computes the max distance between two clusters `c1`and `c2`, using
    `d` as a reference measure
    """
    max_dist = d(c1[0], c2[0])
    for x in c1:
        for y in c2:
            tmp_dist = d(x,y)
            if tmp_dist > max_dist:
                max_dist = tmp_dist
    return(max_dist)


def cmean(c1, c2, d):
    """ computes the mean distance between two clusters `c1`and `c2`, using
    `d` as a reference measure
    """
    scale = float(1) / float(len(c1) * len(c2))
    res = scale * sum(map(lambda x: d(x[0], x[1]), itertools.product(c1,c2)))
    return(res)


def ccent(c1, c2, d):
    """ computes the mean distance between two clusters `c1`and `c2`, using
    `d` as a reference measure
    """

    def vsum(xs):
        """ computes the vectorialized sum of a list of vectors
        example:
        vsum([ [1,2], [3,4], [5,6] ]) => [9, 12]
        """
        new_x = [0 for i in range(len(xs[0]))]
        for x in xs:
            for i in range(len(new_x)):
                new_x[i] = new_x[i] + x[i]
        return(new_x)
    
    nx = map(lambda x: x * float(1) / float(len(c1)),  vsum(c1))
    ny = map(lambda x: x * float(1) / float(len(c2)),  vsum(c2))

    return d(nx, ny)


    
        
        
