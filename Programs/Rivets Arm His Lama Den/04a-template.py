# Rivets Arm His Lama Den
# PART 1
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
	pass

# returns all prime numbers within a min/max range
def getPrimes(min, max):
	primes = []

	for n in range(min, max):
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

# encrypts a message M with a public key K_pub to get C
def encrypt(M, K_pub):
	pass

# decrypts a ciphertext C with a private key K_priv to get M
def decrypt(C, K_priv):
	pass

# MAIN
# get input

# get the primes

# calculate n and z

# get the es and select an e

# calculate d

# generate the public and private keys

# implement RSA in the specified input Ms
