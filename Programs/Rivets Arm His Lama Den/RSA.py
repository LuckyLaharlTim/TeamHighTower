##################################
# Group Name:   Team Hightower
# Members:      Cori Albritton, Megan Cox, Peter Ford, Timothy Oliver
# Assignment:   Program 4 - Rivets Arm His Lama Den (RSA)
# Date:         8 April 2022
##################################

##################################
# Manual
#
# python(3) <fileName>.py < input > output
#
# Flags:
# no flags at the moment
#
#
# NOTE: Currently, the dictionary (or possible dictionaries)
#           MUST be in the same directory as this file
#       
# NOTE2: The program currently takes in input correctly
#        (and decodes correctly if given both e & n -- public key);
#        Unsure if it can find the correct plaintext blind though
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

## given alphabet strings
alph1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

alph2 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

alph3 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "

alph4 = " -,;:!?/.'"+'"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ'

alph5 = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_:./@#$%&*"

alph6 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "

alphTable = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_:./@#$%&*"


# additional alphabets from challenges and such
alph6 = "ABCDEFGHIJ012345abcdefghijklmKLMNOPQRS67nopqrstuvTUVWXYZwxyz89"

alph7 = "ABCDEFGHIJ012345abcdedfhijklmnopKLMNOPQRS67qrstuvwxyTUVWXYZ89z"

#######################
## Variables to Change!
#######################

alphaCandidate = alph4 # <--- CHANGE IF NEEDED
filename = "dictionary-01.txt" # <--- CHANGE IF NEEDED
# keyStartsWith should have strings (or chars) of letters

##################################################

# store characters as elements of list 'alpha'
def makeAlpha():
    alpha = []
    for char in alphaCandidate:
        alpha.append(char)
    letterSize = len(alpha) # size of the alphabet # currently (26 letters)*2 cases + 10 characters + 10 numbers
    return alpha, letterSize

# go through dictionary file and find possible words
def fillDict():
    mDict = []
    f = open(filename, "r")
    for line in f:
        mDict.append(line.strip())
    f.close()
    return mDict

# get alphabet & referencable dictionary
alpha, letterSize = makeAlpha()
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
    return alpha.index(letter)

# returns character in alpha list for given index
def getChar(num):
    return alpha[num]

# make length of x equal to length of y by repeating x
def modifyLen(x,y):
    # check if the x value is a string instead of a list
    #  so we can use 'append'
    xList = []
    for char in x:
        if char in alpha:
            xList.append(char)
    x = xList

    i = 0   
    while len(y)>len(x):
        x.append(x[i])
        i+=1

    return x

# conducts shift of alphabet by given SHIFT positions for each character to cipher text
#  encryption just has the inverse of this in process(message)
def getPlainT(text, key, testing):
    plain = ""
    keyIndex = 0 # if needed

    # shorten ciphertext to shorten the amount of time we
    #  spend making our decision on best plaintext
    if testing:
        mText = []
        limit = math.floor(len(text) * PERCENT)
        for i in range(limit):
            mText.append(text[i])
        text = mText
    
    # for every character . . .
    for i in range(0,len(text)):
        # plaintext character is in alphabet (list/string 'alpha')
        if text[i] in alpha:
            # subtract the key from the character's position in alphabet
            #  and mod by the alphabet size (for negative numbers)
            encodedChar = getChar((getOrdinal(text[i]) - getOrdinal(key[keyIndex])) % letterSize)
            plain += encodedChar
            keyIndex += 1
        # plaintext character is anything else, just repeat the character
        else:
            plain += text[i]
    return plain
          

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

    # get the es and select an e
    try:
        es = [e]
    except NameError:
        es = genEs(z,p,q)
        if "-e" in sys.argv:
            es = [int(sys.argv[sys.argv.index("-e")+1])]
            #es = [choice(es)]
            cipherText = f"{n}\n"
    

    

    ########
    ## END SETUP, START LOOKING 
    ########

    outputStr = ""

    # implement RSA in the specified input Ms
    for i in range(len(es)):

        sys.stdout.write("--\n")
        e = es[i]
        sys.stdout.write("Trying e={}\n".format(e))

        # calculate d
        d = EucModInv(e,z) # d = naiveInverse(e, z)
        if(d==None):
            continue
        sys.stdout.write("d={}\n".format(d))

        # generate the public and private keys
        K_pub = (e, n)
        K_priv = (d, n)
        sys.stdout.write("Public key: {}\n".format(K_pub))
        sys.stdout.write("Private key: {}\n".format(K_priv))
        
        for m in message:
                
            if "-e" in sys.argv:
                m = ord(m)
            else:
                m = int(m)

            # no need to mess with alphabet
            # Message uses ASCII
            if "-e" in sys.argv:
                cipherText += str(encrypt(m, K_pub))+","
            else:
                outputStr += chr(decrypt(m, K_priv))           

        outputStr += "\n"
        
        try:
            #write decrypted text if it has a sizable number of words
            if "-c" in sys.argv:
                sys.stdout.write(outputStr)
            elif "-e" in sys.argv:
                sys.stdout.write(cipherText)
            elif decide(0,outputStr) > len(outputStr.split()) * PERCENT:
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
        

##    if longSearch:
##        sys.stdout.write(f"REMINDER:\ne = {e}\nplaintext=\n{plainText}")

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


    





