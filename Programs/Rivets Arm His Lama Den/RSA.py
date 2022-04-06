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


##  TO-DO: implement percent checks for plain text, decode c-e with program to ensure it's working completely

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
def genEs(z):
	es = []

	for e in range(3, z, 2):
		if (isPrime(e) and gcd(z, e) == 1):
			es.append(e)

	return es

# naively calculates the inverse modulo of e and z
def naiveInverse(e, z):
	d = 0

	while (d < z):
		if ((e * d) % z == 1):
			return d
		d += 1

def factor(num):

    for i in range(3, int(num ** 0.5 + 1), 2):
        if num % i == 0 :
            if isPrime(i) and isPrime(num/i):
                # I guess there will only be one set of prime factors
                print(f"{int(i)}, {int(num/i)}")
                return int(i), int(num/i)
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

# making text
def toText(char):

    return getChar(char % letterSize)
          

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

    outputString = ""

    ########
    ## SETUP
    ########

    # get public key from first line if first line is a tuple
    if message[0][0] == "(":
        tup = message[0].split(",")
        e = int(tup[0][1:])
        n = int(tup[1][:-1])
        K_pub = (e,n)
    # otherwise, take first line as 'n' alone
    elif int(message[0]) == 0:
        pass
    else:
        print(f"n is {message[0]}")
        n = int(message[0])

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
        es = genEs(z)
    

    

    ########
    ## END SETUP
    ########

    outputStr = ""

    # implement RSA in the specified input Ms
    for i in range(len(es)):

        sys.stdout.write("--\n")
        e = es[i]
        #es.remove(e)
        sys.stdout.write("Trying e={}\n".format(e))

        # calculate d
        d = naiveInverse(e, z)
        sys.stdout.write("d={}\n".format(d))

        # generate the public and private keys
        K_pub = (e, n)
        K_priv = (d, n)
        sys.stdout.write("Public key: {}\n".format(K_pub))
        sys.stdout.write("Private key: {}\n".format(K_priv))
        
        for m in message:
            
            if not(m[0] == "("):
                #outputStr += "--\n"
                m = int(m)

                # no need to mess with alphabet
                # Message uses ASCII
                outputStr += chr(decrypt(m, K_priv) % 128)

                # code from example
                '''
                C = encrypt(m, K_pub)
                outputStr += "M={}\n".format(m)
                outputStr += "C={}\n".format(C)
                m = decrypt(C, K_priv)
                outputStr += "M={}\n".format(m)
                '''
            

        try:
##            for char in outputStr:
##                if ord(char) < 32:
##                    sys.stdout.write("ERROR: invalid plaintext.\n")
##                    break
##                else:
##                    sys.stdout.write(outputStr)
##                    break
            if (countThe(outputStr) > 1):
                sys.stdout.write(outputStr)
                # when you only get the proper plaintext
                break
            else:
                sys.stdout.write("ERROR: invalid plaintext.\n")
            
        except UnicodeEncodeError:
                sys.stdout.write("ERROR: invalid plaintext.\n")
        outputStr = ""
        
        
'''
    # decrypting with intent to find most likely plaintext
    if (len(sys.argv) < 2) or (sys.argv[1] not in ["-e","-c"]):
        # check if we want to use non-optimal search criteria (2nd best, etc.)
        if len(sys.argv) > 1:
            simple = False
        else:
            simple = True
        outputList = bestPlainT(text, simple)
        outputString += f"KEY={outputList[1]}:\n"
        outputString += outputList[0]

    # encrypting block (same as getPlainT(ciphertext), but + SHIFT instead
    elif sys.argv[1] == "-e":
        KEY = sys.argv[2]
        KEY = modifyLen(KEY, text)
        keyIndex = 0
        for i in range(0,len(text)):
            # plaintext character is in alphabet (list/string 'alpha')
            if text[i] in alpha:
                encodedChar = getChar(((getOrdinal(text[i]) + getOrdinal(key[keyIndex])) % letterSize))
                outputString += encodedChar
                keyIndex += 1
            # plaintext character is anything else, just repeat the character
            else:
                outputString += text[i]       

    # if you want a decode using a specific shift and not most likely
    elif sys.argv[1] == "-c":
        KEY = sys.argv[2]
        KEY = modifyLen(KEY, text)
        outputString += f"KEY={sys.argv[2]}:\n"+getPlainT(text,KEY,False)
               
'''

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


    





