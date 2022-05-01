# make sure you can get some kind of output

import sys 
import math
import base64
from time import time
from random import choice, randint
from PIL import Image

DEBUGTIME = False
DEBUGMOREFILES = False
showPixels = False
randKey = False

KEY_FILE = "???" 
INPUT_IMAGE = "???"
if DEBUGMOREFILES:
    Thing_IMAGE = "Thing-"+INPUT_IMAGE
else:
    Thing_IMAGE = "Thing-"+INPUT_IMAGE
img = Image.open(INPUT_IMAGE)
img2 = Image.open(INPUT_IMAGE)
pixels = img.load()
Opixels = img2.load()
rows, cols = img.size


def setKey():

    KEY_PIXELS = [[0]*cols]*rows
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

    img.save(Thing_IMAGE)

if __name__ == "__main__":
    if DEBUGTIME:
        t0 = time()


    if (("-x" in sys.argv) or (len(sys.argv) < 2)):
        buildThing()








