"""Functions related to factoring over Z."""

import pickle
import collections
import operator
from functools import reduce

with open('primeData/primeList.pickle', 'rb') as prList:
    orderedPrimes = pickle.load(prList)

def primeDecomposition(N):
    """Return the prime decomposition.

    Parameters
    ----------
    N : int : Number to factor.
    
    Returns
    -------
    primeDecomp : Counter : Prime divisors along with their multiplicity.
    
    Example(s)
    ----------
    >>> primeDecomposition(360)
    >>> Counter({2: 3, 3: 2, 5: 1})
    
    Notes
    -----
    The default upper bound of primes in 'orderedPrimes' is 10,000,000.
    This can be increased in 'generatePrimes.py', but if dealing with
    numbers with suspected prime factors over 10**7, more sophisticated
    techniques can be better suited.

    Due to the upper bound being M = 10**7, the decomposition is
    false iff one of the below:
    
        1. N is prime and N > M**2
        2. The largest prime factor of N is greater than M.

    See Also
    --------
    'decompCertificate' provides a certificate for this decomposition.
        
    """
    if N == 0:
        return collections.Counter()
    
    N = abs(N)
    primeDecomp = collections.Counter()
    for pr in orderedPrimes:
        if pr**2 > N:
            primeDecomp[N] = 1
            break

        q, r = divmod(N, pr)
        while not r:
            N = q
            primeDecomp[pr] += 1
            q, r = divmod(N, pr)

        if N == 1:
            certificate = True
            break

    return primeDecomp

def decompCertificate(N, primeDecomp=False):
    """Return a certificate for any prime decomposition.

    Parameters
    ----------
    N          : int  : Number whose decomposition is being verified.
    primeDecomp: dict : Keys are primes dividing N, values are the multiplicity.
    
    Returns
    -------
    cert : bool : If the decomposition is verifiably certain. 
    
    Example(s)
    ----------
    >>> decompCertificate(37)
    >>> True

    >>> decompCertificate(10, {2:1, 5:2})
    >>> False
    
    Notes
    -----
    If the decomposition method is 'primeDecomposition' function.
    Then 'cert' is false iff one of the below:
    
        1. N is prime and N > M**2
        2. The largest prime factor of N is greater than M.

    Other decomposition methods can result in false decompositions for varied
    reasons.
        
    """
    pDecomp = dict(primeDecomp) if primeDecomp else dict(primeDecomposition(N))
    prod = reduce(operator.mul, map(lambda p: p**pDecomp[p], pDecomp), 1)
    cert = (abs(N) == prod)
    
    return cert

def divisors(N, proper=False):
    """Return a sorted list of all divisors.

    Parameters
    ----------
    N     : int  : Number to factor.
    proper: bool : If including 1 and N. 
    
    Returns
    -------
    divs : list : Ordered list of divisors.
    
    Example(s)
    ----------
    >>> divisors(36)
    >>> [1, 2, 3, 4, 6, 9, 12, 18, 36]

    >>> divisors(36, proper=True)
    >>> [2, 3, 4, 6, 9, 12, 18]

    >>> divisors(7, proper=True)
    >>> []
    
    Notes
    -----
    See 'decompCertificate' for certificate and how to increase likelihood
    of all divisors being listed.
        
    """
    if N == 0:
        return []
    
    N = abs(N)
    primeDecomp = primeDecomposition(N)
    
    allDivisors = {1}
    for pr in primeDecomp:
        newDivisors = set()
        for _ in range(primeDecomp[pr]):
            newDivisors = {factor*pr for factor in allDivisors}
            allDivisors.update(newDivisors)

    if proper:
        allDivisors = allDivisors - {1, N}

    return sorted(allDivisors)

def expOverOne(N):
    """Return prime divisors of N with multiplicity greater than 1.

    Parameters
    ----------
    N : int : Number to factor.
    
    Returns
    -------
    - : dict : Prime factors with multiplicity greater than 1.
    
    Example(s)
    ----------
    >>> expOverOne(360)
    >>> {2: 3, 3: 2}
    
    Notes
    -----
    Assuming GRH the best way to find if a number is square-free
    is (generally) to find the prime-decomposition.

    See Also
    --------
    See the 2015 paper, Detecting Squarefree Numbers by
    Booker, Hiary, and Keating https://arxiv.org/pdf/1304.6937.pdf.

    """
    primeDecomp = dict(primeDecomposition(N))
    return {p: primeDecomp[p] for p in primeDecomp if primeDecomp[p] > 1}
