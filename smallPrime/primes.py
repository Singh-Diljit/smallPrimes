"""Functions related to generating primes over Z."""

import numpy as np
import pickle

def i_modP(p):
    """Return an integer, s.t. its square (mod p) is -1.

    Parameters
    ----------
    p : int : Prime number, s.t. p != 3 (mod 4).
    
    Returns
    -------
    i : int : Integer s.t. i**2 = -1 (mod p)
    
    Example(s)
    ----------
    >>> i_modP(13)
    >>> 8
    
    Notes
    -----
    Such an integer exists for 2 and all odd primes number congruent to 1 mod 4.

    See Also
    --------
    This is used in the 'sumOfSquares' function to express certain primes as
    the sum of squares.
    
    """
    if p == 2:
        i = 1
        
    else:
        N = (p-1) // 2 #p=1 (mod 4) implies N is even.
        for j in range(1, p):
            if pow(j, N, p) == (p-1): #i=sqrt(j**N) satisfies i**2 = -1 (mod p).
                i = pow(j, N//2, p)
                break

    return i

def sumOfSquares(p):
    """Return two integers, with squares summing to input (prime).

    Parameters
    ----------
    p : int : Prime number, s.t. p != 3 (mod 4).
    
    Returns
    -------
    (a, b) : tuple : Integers, a and b, s.t. p = a**2 + b**2.
    
    Example(s)
    ----------
    >>> sumOfSquares(13)
    >>> (3, 2)
    
    Notes
    -----
    This representation of the input as a sum of squares is unique.

    See Also
    --------
    Fermat's theorem on sums of two squares.
    
    """
    if p == 2:
        return (1, 1)
    
    upperBound = int(p ** .5) + 1
    a, b = i_modP(p), p
    while b != 0 and (a > upperBound or b > upperBound):
        a, b = b, a % b

    return (a, b)

def genPrimes(N):
    """Returns primes less than N.

    Parameters
    ----------
    N : int : Upper bound of prime generation, N > 5.
    
    Returns
    -------
    - : array : Array of primes between 2 and N-1 inclusive.
    
    Example(s)
    ----------
    >>> genPrimes(50)
    >>> [ 2  3  5  7 11 13 17 19 23 29 31 37 41 43 47]
    
    Notes
    -----
    This variation of the classic prime sieving method is credited to
    Bruno Astrolino E Silva.
    
    """
    sieve = np.ones(N//3 + (N%6==2), dtype=bool)
    topCheck = int(np.sqrt(N)) // 3
    for i in np.arange(1, topCheck+1):
        if not sieve[i]:
            continue
        k = (3*i + 1)|1
        a = k**2
        b = k * (k - 2*(i&1) + 4)
        sieve[a//3::2*k] = False
        sieve[b//3::2*k] = False

    return np.r_[2,3,((3*np.nonzero(sieve)[0][1:]+1)|1)]

def picklePrimes(N, folderName='primeData'):
    """Save primes under N in three different data structures.

    Parameters
    ----------
    N          : int : Upper bound of prime generation, N > 5.
    folderName : str : Folder data will be written to (must already exist).
    
    Writes
    ------
    primeArray.pickle : array : Ordered primes from 2 to N-1 (dtype=np.int64).
    primeList.pickle  : list  : Ordered primes from 2 to N-1 (dtype=int).
    primeSet.pickle   : set   : Set of primes for easy look-up (dtype=int).
    
    """
    path_ = lambda fileName: f'{folderName}/{fileName}.pickle'
    toSave = genPrimes(N)
    
    with open(path_('primeArray'), 'wb') as f: 
        pickle.dump(toSave, f, pickle.HIGHEST_PROTOCOL)

    with open(path_('primeList'), 'wb') as f: 
        pickle.dump(map(int, toSave), f, pickle.HIGHEST_PROTOCOL)

    with open(path_('primeSet'), 'wb') as f: 
        pickle.dump(set(toSave), f, pickle.HIGHEST_PROTOCOL)

def pickleSumOfSquares(N, folderName='primeData'):
    """Save sum of squares representation of primes, s.t. p != 3 (mod 4), p < N.

    Parameters
    ----------
    N          : int : Upper bound of prime generation, N > 5.
    folderName : str : Folder data will be written to (must already exist).
    
    Writes
    ------
    primeSOS.picke : dict : Keys are primes, values 2-tuples (dtype=int).
    
    """
    path_ = lambda fileName: f'{folderName}/{fileName}.pickle'
    prBank = list(map(int, genPrimes(N)))
    SOSpr = {p:sumOfSquares(int(p)) for p in prBank if p%4 != 3}
    
    with open(path_('primeSOS'), 'wb') as f: 
        pickle.dump(SOSpr, f, pickle.HIGHEST_PROTOCOL)

def pickleAll(N, folderName='primeData'):
    """Save primes under N along with SOS representation.

    Parameters
    ----------
    N          : int : Upper bound of prime generation, N > 5.
    folderName : str : Folder data will be written to (must already exist).
    
    Writes
    ------
    primeArray.pickle : array : Ordered primes from 2 to N-1 (dtype=np.int64).
    primeList.pickle  : list  : Ordered primes from 2 to N-1 (dtype=int).
    primeSet.pickle   : set   : Set of primes for easy look-up (dtype=int).
    primeSOS.picke : dict : Keys are primes, values 2-tuples (dtype=int).
    
    """
    path_ = lambda fileName: f'{folderName}/{fileName}.pickle'
    toSave = genPrimes(N)
    
    with open(path_('primeArray'), 'wb') as f: 
        pickle.dump(toSave, f, pickle.HIGHEST_PROTOCOL)

    toSave = list(map(int, toSave))
    with open(path_('primeList'), 'wb') as f: 
        pickle.dump(toSave, f, pickle.HIGHEST_PROTOCOL)

    with open(path_('primeSet'), 'wb') as f: 
        pickle.dump(set(toSave), f, pickle.HIGHEST_PROTOCOL)

    SOSpr = {p:sumOfSquares(int(p)) for p in toSave if p%4 != 3}
    with open(path_('primeSOS'), 'wb') as f: 
        pickle.dump(SOSpr, f, pickle.HIGHEST_PROTOCOL)
