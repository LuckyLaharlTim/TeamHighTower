##################################
# Group Name:   Team Hightower
# Members:      Cori Albritton, Megan Cox, Peter Ford, Timothy Oliver
# Assignment:   Program 5 - XOR ROX (XOR, Bitwise Operators)
# Date:         29 April 2022
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
from PIL import Image

# variables for debug lines and extra things
DEBUGTIME = True

# the image variables
KEY_FILE = "05-key.txt"
INPUT_IMAGE = "05-xor.png"#"input.png"
AND_IMAGE = "and-"+INPUT_IMAGE
OR_IMAGE = "or-"+INPUT_IMAGE
XOR_IMAGE = "xor-"+INPUT_IMAGE
img = Image.open(INPUT_IMAGE)
img2 = Image.open(INPUT_IMAGE)
pixels = img.load()
Opixels = img2.load()
rows, cols = img.size

def setKey():

    KEY_PIXELS = [[0]*cols]*rows
    # fills KEY_PIXELS
    f = open(KEY_FILE)
##    pixelRow = 0
##    pixelCol = 0
    line = f.readline().strip()
    for row in range(rows):
        for col in range(cols):
            line = line.split(",")
            KEY_PIXELS[row][col] = int(line[0]), int(line[1]), int(line[2])
            line = f.readline().strip()
            
##    while not (line == None):
##        line = line.split(",")
##        KEY_PIXELS.append((int(line[0]), int(line[1]), int(line[2])))
##        line = f.readline().strip()
    f.close()
    return KEY_PIXELS

KEY_PIXELS = setKey()      

def buildAND():
        
    for row in range(rows):
        for col in range(cols):
            Or,Og,Ob = Opixels[row,col]
            Kr,Kg,Kb = KEY_PIXELS[row][col]
            r = Or & Kr
            g = Og & Kg
            b = Ob & Kb
            pixels[row,col] = r,g,b

    # write the new image
    img.save(AND_IMAGE)

def buildOR():
    
    for row in range(rows):
        for col in range(cols):
            Or,Og,Ob = Opixels[row,col]
            Kr,Kg,Kb = KEY_PIXELS[row][col]
            r = Or | Kr
            g = Og | Kg
            b = Ob | Kb
            pixels[row,col] = r,g,b

    # write the new image
    img.save(OR_IMAGE)

def buildXOR():
    
    for row in range(rows):
        for col in range(cols):
            Or,Og,Ob = Opixels[row,col]
            Kr,Kg,Kb = KEY_PIXELS[row][col]
            r = Or ^ Kr
            g = Og ^ Kg
            b = Ob ^ Kb
            pixels[row,col] = r,g,b

    # write the new image
    img.save(XOR_IMAGE)

########
### MAIN
########


# differentiate between arguments of encoding or decoding
if __name__ == "__main__":
    if DEBUGTIME:
        t0 = time()

    #buildAND()
    #buildOR()
    buildXOR()
    
    if DEBUGTIME:
        t1= time()
        timedelta = t1-t0
        sys.stdout.write(f"\nOutput written after {timedelta} seconds")


    





