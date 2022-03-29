##################################
# Group Name:   Team Hightower
# Members:      Cori Albritton, Megan Cox, Peter Ford, Timothy Oliver
# Assignment:   Program 3 - Le Chiffre (Vigenere Cipher)
# Date:         8 April 2022
##################################

##################################
# Manual
#
# python(3) <fileName>.py <flag> <KEY> < input > output
#
# Flags:
# -e | will encode input and write to output
#      or terminal if input/output not provided
# 'no flag' | will decode input and write most likely plaintext to output
#      or terminal if input/output not provided
# -c | will decode input using specified KEY and write to output
#      or terminal if input/output not provided
#
#
# NOTE: Currently, the dictionary (or possible dictionaries)
#           MUST be in the same directory as this file
#       
# NOTE2: if nothing is working, try changing
#           alphaCandidate (the alphabet) or filename (the dictionary)
##################################


##  TO-DO: implement percent checks for plain text, decode c-e with program to ensure it's working completely

import sys # import sys for standard input from command line
import math
import base64

# variables for debug lines and showing the bestShifts if we need to
#  find doubly -> multiply encrypted plaintext
DEBUG = False
DEBUG2 = False
DISPLAY_SHIFTS = False
PERCENT = 0.3
DECIDEFUNCTION = 0
# 0 - most dictionary matches
# 1 - most occurences of word 'the'

## given alphabet strings
alph = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

alph1 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"

alph2 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "

alph3 = " -,;:!?/.'"+'"()[]$&#%012345789aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxyYzZ'

alph4 = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_:./@#$%&*"

alph5 = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789`~!@#$%^&*()-_=+[{]}\|;:'\",<.>/? "

alphTable = "abcdefghijklmnopqrstuvwxyz0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ_:./@#$%&*"


# additional alphabets from challenges and such
alph6 = "ABCDEFGHIJ012345abcdefghijklmKLMNOPQRS67nopqrstuvTUVWXYZwxyz89"

alph7 = "ABCDEFGHIJ012345abcdedfhijklmnopKLMNOPQRS67qrstuvwxyTUVWXYZ89z"

#######################
## Variables to Change!
#######################

alphaCandidate = alph3 # <--- CHANGE IF NEEDED
filename = "dictionary-01d.txt" # <--- CHANGE IF NEEDED
keyStartsWith = [] # <--- CHANGE (list) IF NEEDED

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
    
# decode code (done for each possibility in the alphabet)
#  given cipher text and boolean to determine
#  if we are using decision criteria once or more
def bestPlainT(text, simple):
    bestKeyWords = 0 # integer value of number of real words
                     #  in string with most dictionary matches
    bestKey = "" # string value of keyword with most real words
    words = [] # list of attempted keywords
    wordCounts = [] # list of dictionary word matches for each possible shift
##    if not simple:
##        nMostWords = int(sys.argv[2]) # the number of times we go down
##                                      #  our decision variable for multiple encryptions
##                                      # ex: 3rd most word matches,
##                                      #  2nd most words at beginning of new line, etc. 

    # would put IDEA here

    # find number of (real words, the's, etc.)
    #  using each possible word in dictionary
    for word in miniDict:
        skipWord = False
        if (len(keyStartsWith) > 0) and (word[0] not in keyStartsWith):
            skipWord = True
      
        if not skipWord:
            posPlain = getPlainT(text,modifyLen(word, text),True)
##            if getAll:
##                filename = f"key{i}.txt"
##                f = open(filename, "w")
##                f.write(posPlain)
##            elif not getAll:
            # could be countWords, countThe, etc.
            wordCount = decide(DECIDEFUNCTION,posPlain)
            wordCounts.append(wordCount)
            words.append(word)

    # get the index of the most likely plain text
    bestKeyWords = max(wordCounts)
    bestKey = words[wordCounts.index(bestKeyWords)]
##    if not simple:
##        for n in range(nMostWords):
##            wordCounts[bestShift] = 0
##            bestShiftWords = max(wordCounts)
##            bestShift = wordCounts.index(bestShiftWords)
##            if DISPLAY_SHIFTS:
##                sys.stdout.write(f"reached 'not simple'; current bestShift: {bestShift}")
            
        
    # return everything for display
    #  (most likely plaintext & the alphabet shift used to obtain it)
    return [getPlainT(text, modifyLen(bestKey,text), False), bestKey]

    ##########
    # IDEA
    ##########
    #
    #   We could try using all possible alphabets and returning
    #       the most likely plain text of them all.
    #   At the moment, it will add too much time to texts like 01c or 01d

    # iterate through all possible shifts and use
    #  most likely plaintext decision criteria
            

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

    text = []
    outputString = ""

    # put each individual character in a list (for comparison w/ characters in key)
    for char in message:
        text.append(char)

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
               


    # output the appropriate message
    sys.stdout.write(outputString)

########
### MAIN
########


# differentiate between arguments of encoding or decoding
if __name__ == "__main__":
    message = sys.stdin.read()
    process(message)
