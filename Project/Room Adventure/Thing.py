##################################
# Group Name:   Team Hightower
# Members:      Cori Albritton, Megan Cox, Peter Ford, Timothy Oliver
# Assignment:   Program 5 - Thing ROX (Thing, Bitwise Operators)
# Date:         29 April 2022
##################################

##################################
# Manual
#
# python(3) <fileName>.py <flag(s)>  > output
#
# Flags:
# no flag | will create AND, OR, & Thing versions of the INPUT_IMAGE in the current directory
#   
# -x | will create an Thing version of the INPUT_IMAGE in the current directory and etc.
#
# NOTE: flags can be used together
#       
# NOTE2: The program currently achieves its objective,
#         but results differ from files like '05-or.png' received from Digilormo
#         (also Thinging a Thing output is the same visually,
#         but is larger in size than original)
##################################

import sys # import sys for standard input from command line
import math
import base64
from time import time
from random import choice, randint
from PIL import Image

# variables for debug lines and extra things
DEBUGTIME = False
DEBUGMOREFILES = False
showPixels = False
randKey = False

# the image variables
KEY_FILE = "key.txt" # messes up the given key file, but preserves ones it makes
INPUT_IMAGE = "weirdPhoto.png"#"input.png"
if DEBUGMOREFILES:
    Thing_IMAGE = "Thing-"+INPUT_IMAGE
else:
    Thing_IMAGE = "Thing-"+INPUT_IMAGE
img = Image.open(INPUT_IMAGE)
img2 = Image.open(INPUT_IMAGE)
pixels = img.load()
Opixels = img2.load()
#sys.stdout.write(f"[{INPUT_IMAGE} is loaded]")
##if showPixels:
##    for val in pixels:
##        sys.stdout.write(val)
rows, cols = img.size
# print(f"there are {rows*cols} pixels")

def setKey():

    KEY_PIXELS = [[0]*cols]*rows

    
    # fills KEY_PIXELS
    if randKey:
        for row in range(rows):
            for col in range(cols):
                KEY_PIXELS[row][col] = randint(0,255), randint(0,255), randint(0,255)

    else:
        f = open(KEY_FILE)

        line = f.readline().strip()
        for row in range(rows):
            for col in range(cols):
                line = line.split(",")
                KEY_PIXELS[row][col] = int(line[0]), int(line[1]), int(line[2])
                line = f.readline().strip()
    ##            if x==0:
    ##                print(KEY_PIXELS[row][col])
    ##            x+=1
                

        f.close()
    return KEY_PIXELS

KEY_PIXELS = setKey()




def buildThing():
    
    for row in range(rows):
        for col in range(cols):
            Or,Og,Ob = Opixels[row,col]
            Kr,Kg,Kb = KEY_PIXELS[row][col]
            r = Or ^ Kr
            g = Og ^ Kg
            b = Ob ^ Kb
            pixels[row,col] = r,g,b

    # write the new image
    img.save(Thing_IMAGE)

########
### MAIN
########


# differentiate between arguments of encoding or decoding
if __name__ == "__main__":
    if DEBUGTIME:
        t0 = time()


    if (("-x" in sys.argv) or (len(sys.argv) < 2)):
        buildThing()
##        outputS += f"{Thing_IMAGE},"







