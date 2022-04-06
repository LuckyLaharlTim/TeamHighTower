# Rivets Arm His Lama Den
# Implements a simplistic RSA algorithm with the following characteristics:
# -expect input to contain the public key on the first line and a comma separated list of numbers representing encrypted values on the second line
# -the input provides n and e
# -write a function that determines if a number is prime
# -write a function that factors a number into the product of two primes
# -write a function that recursively calculates the greatest common divisor of a and b
# -write a function that naively calculates d, the modulo inverse of e
# -write a decrypt function that decrypts ciphertext C with the private key to get M
# -factor n as the product of two primes, p and q
# -calculate z = ((p - 1) * (q - 1)) / gcd(p - 1, q - 1)
# -calculate d as the inverse modulo of e
# -output the public and private keys
# -decrypt each value from the input using the private key to generate a valid ASCII character
# -rebuild the original message

# determines if a given number is prime
def isPrime(n):
	pass

# factors a number n into the product of two primes
def factor(n):
	pass

# recursively returns the greatest common divisor of a and b
def gcd(a, b):
	pass

# naively calculates the inverse modulo of e and z
def naiveInverse(e, z):
	pass

# decrypts a ciphertext C with a private key K_priv to get M
def decrypt(C, K_priv):
	pass

# MAIN
# get input

# grab the public key and ciphertext values
# isolate e and n from the public key

# factor n into p and q
# calculate z

# calculate d

# generate the private key

# implement RSA for the specified input Cs
