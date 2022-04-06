# Rivets Arm His Lama Den
# PART 1 (IN CLASS WITH STUDENTS)
# Implements a simplistic RSA algorithm with the following characteristics:
# -let's restrict ourselves to "small" numbers
# -write a function that determines if a number is prime
# -write a function that generates all prime numbers within some given range
# -randomly select two of the primes
# -calculate n = p * q
# -write a function that recursively calculates the greatest common divisor of a and b
# -calculate z = ((p - 1) * (q - 1)) / gcd(p - 1, q - 1)
# -write a recursive gcd function
# -write a function that generates all e's and randomly selects one (using isPrime and gcd)
# -write a function that naively calculates d, the modulo inverse of e
# -output the public and private keys
# -write an encrypt function that encrypts message M with the public key to get C
# -write a decrypt function that decrypts ciphertext C with the private key to get M

from sys import stdin
from random import choice

# the min and max range for prime number generation
MIN_PRIME = 100
MAX_PRIME = 999

# determines if a given number is prime
def isPrime(n):
	if (n % 2 == 0):
		return False

	for i in range(3, int(n ** 0.5 + 1), 2):
		if (n % i == 0):
			return False

	return True

# returns all prime numbers within a min/max range
def getPrimes(MIN_PRIME, MAX_PRIME):
	primes = []

	for n in range(MIN_PRIME, MAX_PRIME):
		if (isPrime(n)):
			primes.append(n)

	return primes


# generates all e's and randomly returns one
def genEs(z):
	es = []

	for e in range(3, z, 2):
		if (isPrime(e) and gcd(z, e) == 1):
			es.append(e)

	return es

# recursively returns the greatest common divisor of a and b
def gcd(a, b):
	if (b == 0):
		return a

	return gcd(b, a % b)

# naively calculates the inverse modulo of e and z
def naiveInverse(e, z):
	d = 0

	while (d < z):
		if ((e * d) % z == 1):
			return d
		d += 1
'''
# calculates the inverse modulo of e and z
def EuclideanInverse(e,z):
        if e == 0:
                return z, 0, 1

        gcd, s1, t1 = EuclideanInverse
'''
# encrypts a message M with a public key K_pub to get C
def encrypt(M, K_pub):
	return (M ** K_pub[0]) % K_pub[1]

# decrypts a ciphertext C with a private key K_priv to get M
def decrypt(C, K_priv):
	return (C ** K_priv[0]) % K_priv[1]

# MAIN
M = stdin.read().rstrip("\n").split("\n")

# get the primes
primes = getPrimes(MIN_PRIME, MAX_PRIME)
p = choice(primes)
q = p
while (q == p):
	q = choice(primes)
print "p={}, q={}".format(p, q)

# calculate n and z
n = p * q
print "n={}".format(n)
z = ((p - 1) * (q - 1)) / gcd(p - 1, q - 1)
print "z={}".format(z)

# get the es and select an e
es = genEs(z)
e = choice(es)
print "e={}".format(e)

# calculate d
d = naiveInverse(e, z)
print "d={}".format(d)

# generate the public and private keys
K_pub = (e, n)
K_priv = (d, n)
print "Public key: {}".format(K_pub)
print "Private key: {}".format(K_priv)

# implement RSA in the specified input Ms
for m in M:
	print "--"
	m = int(m)
	C = encrypt(m, K_pub)
	print "M={}".format(m)
	print "C={}".format(C)
	m = decrypt(C, K_priv)
	print "M={}".format(m)

