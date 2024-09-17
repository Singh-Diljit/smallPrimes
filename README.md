# smallPrimes

smallPrimes is used to precompute primes under $N = 10^8$ in three different data structures. In addition,
for each $p \cong 1 \pmod 4$, the expression of $p$ as a sum of squares is saved. Also included are functions related to the prime decomposition, and factorization of integers.

smallPrimes is used to support more complex factorization and primality related modules, where taking care of small prime cases can greatly increase more costly functions.

In particular, the prime decomposition function acts as a prime certificate for an integer $M$ giving a premature positive if:
	1. $M$ is prime and $M > N^2 = 10^{16}$
and a false positive if:
	2. The largest prime factor $M$ is greater than $N = 10^8$.
## Usage

```python
#Express a prime congruent to 1 mod 4 as a sum of squares.
sumOfSquares(13)
>>> (3, 2)

#Returns primes less than N.
genPrimes(50)
>>> [ 2  3  5  7 11 13 17 19 23 29 31 37 41 43 47]

#Return the prime decomposition.
primeDecomposition(360)
>>> Counter({2: 3, 3: 2, 5: 1})

#Return a certificate for a prime decomposition.
decompCertificate(37)
>>> True

#Return a sorted list of all divisors.
divisors(36)
>>> [1, 2, 3, 4, 6, 9, 12, 18, 36]

divisors(36, proper=True)
>>> [2, 3, 4, 6, 9, 12, 18]
```
