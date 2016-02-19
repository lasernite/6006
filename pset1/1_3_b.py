        
# Code for stock problem (L01, 6.006 MIT EECS)

"""
You are given an array A[0..n-1] of stock prices for
n consecutive days, and want to pick two days i0 and j0,
with 0 <= i0 <= j0 < n such if you buy a share of stock on day
i0 and sell it on day j0 you have maximum gain.  That is,
you want to maximize  A[j0] - A[i0].

The routines 'naive', 'dc', and 'lin' implement a naive
algorithm, a divide-and-conquer algorithm, and a linear-time
algorithm. 

These routines only return the maximum gain possible; they
don't return the days i0 and j0 that achieve this gain.

Exercise: modify these routines to output i0 and j0 as well.

"""

import random
import time

def make_prices(n, seed):
    """ Return array of n random prices, based on seed. """
    random.seed(seed)              # set random # generator seed
    return [ random.random() for _ in range(n) ]

def naive(A):
    """ return best gain on A, using naive method 
        running time, due to doubly-nest loop, is Theta(n^2)
    """
    n = len(A)
    ans = 0
    index = [0,0]
    for i in range(n):
        for j in range(i,n):
            ans = max(ans, A[j]-A[i])
            if ans > A[index[1]] - A[index[0]]:
                index[0] = i
                index[1] = j

    index2 = [0,0]
    ans2 = 0
    for i in range(n):
        for j in range(i, n):
            if (i >= index[1] and j >= index[1]) or (i <= index[0] and j <= index[0]):
                ans2 = max(ans2, A[j] - A[i])
                if ans2 > A[index2[1]] - A[index2[0]]:
                    index2[0] = i
                    index2[1] = j

    return (ans, ans2, index, index2)

def dc(A, lo, hi):
    """ return best gain on A[lo:hi], using divide & conquer 
        running time is solution to T(n) = 2*T(n/2) + Theta(n) = Theta(n log n)
    """
    n = hi-lo
    # base case
    if n == 1:
        return 0
    # divide and conquer
    # divide into lo:mid and mid:hi
    mid = (lo+hi)//2            
    # recurse on left half
    gain_low = dc(A, lo, mid)
    # recurse on right half
    gain_high = dc(A, mid, hi)
    # figure out best gain for buying in left half, selling in right half
    buy_price = min([ A[i] for i in range(lo, mid) ])
    sell_price = max([ A[i] for i in range(mid, hi)])
    gain_cross = sell_price - buy_price
    # optimum is max of three cases just solved
    return max(gain_low, gain_high, gain_cross)

def lin(A):
    """ return two best gains, computed by simple linear-time alg 
        running time is Theta(n)
    """
    n = len(A)
    # precompute all prefix minimas
    # PMin[i] is the minimum in the length i+1 prefix of A
    PMins = [0] * n
    PMins[0] = A[0]
    biggest = max(A)
    # i, j
    index = [0,0]
    for i in range(1, n):
        PMins[i] = min(A[i], PMins[i-1])

    # max_gain will equal the optimum gain max_{i} max_{j>=i} A[j]-A[i]
    max_gain = 0
    for j in range(1, n):
        if max_gain < A[j]-PMins[j]:
            sell_point = j
        max_gain = max(max_gain, A[j]-PMins[j]) 
    

    buy_point = PMins.index(PMins[sell_point])
    # get second best gain
    PMins2 = PMins[:]
    for i in range(1, n):
        if PMins2[i] == PMins[sell_point]:
            # Make pmin largest so it doesn't get used again
            PMins2[i] = biggest

    max_gain_2 = 0
    for j in range(1, buy_point):
        max_gain_2 = max(max_gain_2, A[j]-PMins2[j]) 

    max_gain_3 = 0
    for j in range(sell_point, len(A)):
        max_gain_3 = max(max_gain_3, A[j]-PMins2[j])


    return max_gain, max(max_gain_2, max_gain_3)

def test():

    n = 10000            # may want to use pypy for larger value of n
    print "n = ", n
    A = make_prices(n, 1)

    t0 = time.time()
    gain_naive = naive(A)
    t1 = time.time()
    gain_dc = dc(A,0,n)
    t2 = time.time()
    gain_lin = lin(A)
    t3 = time.time()

    print "naive: ", gain_naive, "time: ", t1-t0, " seconds."
    print "dc:    ", gain_dc,    "time: ", t2-t1, " seconds."
    print "lin:   ", gain_lin,   "time: ", t3-t2, " seconds."

test()

""" Typical output:
    n =  10000
    naive:  0.999714239084 time:  8.96542191505  seconds.
    dc:     0.999714239084 time:  0.0268700122833  seconds.
    lin:    0.999714239084 time:  0.00327301025391  seconds.
"""
  
