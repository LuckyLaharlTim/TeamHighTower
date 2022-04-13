##################################
# Group Name:   Team Hightower
# Members:      Cori Albritton, Megan Cox, Peter Ford, Timothy Oliver
# Assignment:   Program 4 - Rivets Arm His Lama Den (RSA)
# Date:         8 April 2022
##################################

##################################
# Manual
#
# python(3) <fileName>.py <flags> <e> < input > output
#
# Flags:
# no flag | will decrypt input using all possible e's until a readable on is obtained,
#            initially knowing only the n value;
#            will use Fermat's numbers as e value first
#
# -c | will decrypt input using the specified e in command line;
#       output generated regardless of readability
#
# -e | in progress; should encode readable text into int values with n first
#       uses given e value for public and private keys
#
# NOTE: Currently, the dictionary (or possible dictionaries)
#           MUST be in the same directory as this file
#       
# NOTE2: The program currently takes in input correctly
#        (and decodes correctly if given both e & n -- public key);
#        Unsure if it can quickly find the correct plaintext blind though
##################################



import sys # import sys for standard input from command line
import math
import base64
from time import time
from random import choice, randint

# variables for debug lines and showing the bestShifts if we need to
#  find doubly -> multiply encrypted plaintext
DEBUG = False
DEBUG2 = False
DISPLAY_SHIFTS = False
DEBUGTIME = True

SET_P_Q = False
p = 389
q = 683
SEPARATED_BY = "," # often "," or "\n"
CUTOFFBYDICTMATCH = True
longSearch = True # <- will stop as soon as we find a decent plainText
AVG_LENGTH = 5
PERCENT = 0.3
MIN_PRIME = 100
MAX_PRIME = 999
DECIDEFUNCTION = 0
# 0 - most dictionary matches
# 1 - most occurences of word 'the'

#######################
## Variables to Change!
#######################

filename = "dictionary-01.txt" # <--- CHANGE IF NEEDED

##################################################

# go through dictionary file and find possible words
def fillDict():
    mDict = []
    f = open(filename, "r")
    for line in f:
        mDict.append(line.strip())
    f.close()
    return mDict

# get referencable dictionary
miniDict = fillDict()

###########################
## RSA (Prime #) Functions
###########################

# determines if a given number is prime
def isPrime(n):
	if (n % 2 == 0):
		return False

	for i in range(3, int(n ** 0.5 + 1), 2):
		if (n % i == 0):
			return False

	return True

# recursively returns the greatest common divisor of a and b
def gcd(a, b):
	if (b == 0):
		return a

	return gcd(b, a % b)
    
# returns all prime numbers within a min/max range
def getPrimes(MIN_PRIME, MAX_PRIME):
	primes = []

	for n in range(MIN_PRIME, MAX_PRIME):
		if (isPrime(n)):
			primes.append(n)

	return primes


# generates all e's and randomly returns one
def genEs(z, p, q):
    es = [3,5,17,257,65537]
    for e in es:
        if e > z:
            es.remove(e)
    
    # put in special primes as first 'e' value we test
    # (remove them if they are greater than the z we use)

    # source for ideas to speed up finding e:
    #   https://crypto.stackexchange.com/questions/13166/method-to-calculating-e-in-rsa

    for e in range(max(p,q), z, 2):
        if (isPrime(e) and gcd(z, e) == 1 and e not in es):
            es.append(e)

    # in case e is one of those earlier possibilities
    for e in range(7, max(p,q), 2):
        if (isPrime(e) and gcd(z, e) == 1 and e not in es):
            es.append(e) 

    return es

# calculates the inverse modulo of e and z
# grabbed from here: https://www.packetmania.net/en/2022/01/22/Python-Textbook-RSA/
def extgcd(e,z):
        old_s, s = 1, 0
        old_t, t = 0,1

        while z:
            x = e // z
            s, old_s = old_s - x * s, s
            t, old_t = old_t - x * t, t
            e,z = z, e%z
        return e, old_s, old_t


    
# naively calculates the inverse modulo of e and z
def naiveInverse(e, z):
	d = 0

	while (d < z):
		if ((e * d) % z == 1):
			return d
		d += 1

# shoulde find mod inverse using Extended Eucliedean Algorithm
# also grabbed from here: https://www.packetmania.net/en/2022/01/22/Python-Textbook-RSA/
def EucModInv(e,z):

    g,x,y = extgcd(e,z)
    try:
        assert g == 1

        if x < 0:
            x += z
        return x
    except AssertionError:
        return naiveInverse(e,z)

def factor(num):

    for i in range(3, int(num ** 0.5 + 1), 2):
        if num % i == 0 :
            if isPrime(i) and isPrime(num/i):
                # I guess there will only be one set of prime factors
                return int(i), int(num/i)


# encrypts a message M with a public key K_pub to get C
def encrypt(M, K_pub):
	return (M ** K_pub[0]) % K_pub[1]

# decrypts a ciphertext C with a private key K_priv to get M
def decrypt(C, K_priv):
	return (C ** K_priv[0]) % K_priv[1]


## UNNEEDED
# check if a letter is uppercase or lowercase (or a number);
#  moreso for when 'A' and 'a' are considered equal
def checkCase(letter):
    if ((ord(letter) > 64) and (ord(letter) < 91)):
        return "upper"
    elif ((ord(letter) > 96) and (ord(letter) < 123)):
        return "lower"
    elif ((ord(letter) > 47) and (ord(letter) < 58)):
        return "number"
    else:
        return None

# function to determine cutoff point for word matches for early output
def checkThreshold(posPlain, wordCount):
    
    threshold = len(posPlain.split())//AVG_LENGTH
    expectedWords = math.floor(len(posPlain.split()) * PERCENT)

    if wordCount > expectedWords:
        return True
    return False
                           

# function that runs appropriate 'best plain text' function
#  ~ all current functions look for the plaintext with the most of something
# parameter(s): func - int variable above corresponding to function to run
#               a - the potential plaintext (a string)
def decide(func, a):
    if not func: # or func == 0
        return countWords(a)
    if func == 1:
        return countThe(a)

# returns position in alpha list for given character
def getOrdinal(letter):
    return ord(letter)

# returns character in alpha list for given index
def getChar(num):
    return chr(num)
         

# function to count the words in text
#  that are also in specified dictionary
def countWords(posPlain):
    wordCount = 0
    words = posPlain.split()
    for word in words:
        if word in miniDict:
            wordCount += 1

    
    return wordCount


# function to count the's in text
#  that are also in specified dictionary
def countThe(posPlain):
    wordCount = 0
    words = posPlain.split()
    for word in words:
        if word in ["The", "the"]:
            wordCount += 1

    
    return wordCount

#############
# IN PROGRESS
#############
# function to count the's in text
#  that are also in specified dictionary
def countLets(posPlain, alpha):
    lets = [0]*len(alpha)
    for char in posPlain:
        lets[getOrdinal(char)] += 1

    
    return lets
#####################################

## build ciphertext using readable input characters
def makeCipher(e,n,p,q,z,message):
    outputStr = ""
    K_pub = (e, n)

    for m in message:
        m = ord(m)

        # no need to mess with alphabet
        # Message uses ASCII
        outputStr += str(encrypt(m, K_pub))+","         

    outputStr = outputStr[:-1] # get rid of last comma
    sys.stdout.write(f"{n}\n{outputStr}")

## given a public key, decrypt input numbers to plaintext
def getPlainE(e,n,p,q,z,message):
    outputStr = ""

    sys.stdout.write("--\n")
    sys.stdout.write("Trying e={}\n".format(e))

    # calculate d
    d = EucModInv(e,z)
    sys.stdout.write("d={}\n".format(d))

    # generate the public and private keys
    K_pub = (e, n)
    K_priv = (d, n)
    sys.stdout.write("Public key: {}\n".format(K_pub))
    sys.stdout.write("Private key: {}\n".format(K_priv))
    
    for m in message:
        m = int(m)

        # no need to mess with alphabet
        # Message uses ASCII
        outputStr += chr(decrypt(m, K_priv))           

    outputStr += "\n"
    
    try:
        #write decrypted text if it has a sizable number of words
        sys.stdout.write(outputStr)
    except UnicodeEncodeError:
        sys.stdout.write("ERROR: invalid plaintext.\n")

## given only n, decrypt input numbers to plaintext
def getPlain(n,p,q,z,message):
    outputStr = ""

    # get possible e's --change genEs() to modify what's tried first
    es = genEs(z,p,q)

    # implement RSA in the specified input Ms
    for i in range(len(es)):

        sys.stdout.write("--\n")
        e = es[i]
        sys.stdout.write("Trying e={}\n".format(e))

        # calculate d
        d = EucModInv(e,z)
        if(d==None):
            d = naiveInverse(e, z) # error with modified function to find ModInv
            if(d==None):
                sys.stdout.write(f"No modular inverse found for e = {e}\n")
                continue # can just skip current e altogether instead
        sys.stdout.write("d={}\n".format(d))

        # generate the public and private keys
        K_pub = (e, n)
        K_priv = (d, n)
        sys.stdout.write("Public key: {}\n".format(K_pub))
        sys.stdout.write("Private key: {}\n".format(K_priv))
        
        for m in message:
            m = int(m)

            # no need to mess with alphabet
            # Message uses ASCII
            outputStr += chr(decrypt(m, K_priv))           

        outputStr += "\n"
        
        try:
            #write decrypted text if it has a sizable number of words
            if decide(0,outputStr) > len(outputStr.split()) * PERCENT:
                sys.stdout.write(outputStr)
                if longSearch:
                    plainText = outputStr
            else:
                sys.stdout.write("ERROR: invalid plaintext.\n")
        except UnicodeEncodeError:
                sys.stdout.write("ERROR: invalid plaintext.\n")
                
        outputStr = ""

        if longSearch:
            try:
                len(plainText) > 5
                break
            except NameError:
                continue
    

# function to process message (encrypting, decrypting most likely plaintext,
#  or simply decrypting with a stated shift
def process(message):

    ########
    ## SETUP
    ########

    
    if message[0][0] == "(":
        tup = message[0].split(",")
        e = int(tup[0][1:])
        n = int(tup[1][:-1])
    # otherwise, take first line as 'n' alone
    elif int(message[0]) == 0:
        pass
    else:
        if "-c" in sys.argv:
            e = int(sys.argv[sys.argv.index("-c")+1])
        n = int(message[0])
    message = message[1:]

    
    # if we already have n (we should), find p and q  
    try:
        p,q = factor(n)
    except NameError:
        primes = getPrimes(MIN_PRIME, MAX_PRIME)
        p = choice(primes)
        q = p
        while (q == p):
                q = choice(primes)
        n = p*q
        
    sys.stdout.write(f"p={p}, q={q}\n")
    sys.stdout.write(f"n={n}\n")
    z = int(((p - 1) * (q - 1)) / gcd(p - 1, q - 1))
    sys.stdout.write(f"z={z}\n")

    if "-e" in sys.argv:
        str = ""
        for val in message:
            str += val
        makeCipher(int(sys.argv[sys.argv.index("-e")+1]), n, p, q, z, str)
    else:
        try:
            getPlainE(e,n,p,q,z,message)
        except:
            getPlain(n,p,q,z,message)
    
    ########
    ## END SETUP, START LOOKING 
    ########

########
### MAIN
########


# differentiate between arguments of encoding or decoding
if __name__ == "__main__":
    if DEBUGTIME:
        t0 = time()
    inpt = sys.stdin.read().rstrip("\n")
    
    # for getting proper message
    message = inpt.split("\n",1)
    intermediate = message[1]
    message = message[0:1]
    for num in intermediate.split(SEPARATED_BY):
        message.append(num)
    
    process(message)
    if DEBUGTIME:
        t1= time()
        timedelta = t1-t0
        sys.stdout.write(f"\nOutput written after {timedelta} seconds")


    





