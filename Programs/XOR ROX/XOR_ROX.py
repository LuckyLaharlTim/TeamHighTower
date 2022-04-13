##################################
# Group Name:   Team Hightower
# Members:      Cori Albritton, Megan Cox, Peter Ford, Timothy Oliver
# Assignment:   Program 5 - XOR ROX (XOR, Bitwise Operators)
# Date:         29 April 2022
##################################

##################################
# Manual
#
# python(3) <fileName>.py <flag(s)> < input > output
#
# Flags:
# no flag | will create AND, OR, & XOR versions of the INPUT_IMAGE in the current directory
#
# -a | will create an AND version of the INPUT_IMAGE in the current directory       
#
# -o | will create an OR version of the INPUT_IMAGE in the current directory
#       
# -x | will create an XOR version of the INPUT_IMAGE in the current directory 
#
# NOTE: flags can be used together
#       
# NOTE2: The program currently achieves its objective,
#         but results differ from files like '05-or.png' received from Digilormo
#         (also XORing a xor output is the same visually,
#         but is larger in size than original)
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
INPUT_IMAGE = "input.png"#"input.png"
AND_IMAGE = "and-"+INPUT_IMAGE
OR_IMAGE = "or-"+INPUT_IMAGE
XOR_IMAGE = "xor-"+INPUT_IMAGE
img = Image.open(INPUT_IMAGE)
pixels = Opixels = img.load()
rows, cols = img.size
# print(f"there are {rows*cols} pixels")

def setKey():

    KEY_PIXELS = [[0]*cols]*rows
    # print(f"there are {len(KEY_PIXELS)*len(KEY_PIXELS[0])} pixels in KEY_PIXELS")
    # fills KEY_PIXELS
    f = open(KEY_FILE)

    line = f.readline().strip()
    for row in range(rows):
        for col in range(cols):
            line = line.split(",")
            KEY_PIXELS[row][col] = int(line[0]), int(line[1]), int(line[2])
            line = f.readline().strip()
            

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

    if (("-a" in sys.argv) or (len(sys.argv) < 2)):
        buildAND()
    if (("-o" in sys.argv) or (len(sys.argv) < 2)):
        buildOR()
    if (("-x" in sys.argv) or (len(sys.argv) < 2)):
        buildXOR()
    
    if DEBUGTIME:
        t1= time()
        timedelta = t1-t0
        sys.stdout.write(f"\nOutput written after {timedelta} seconds")


    





