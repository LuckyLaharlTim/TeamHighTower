###########################################################################################
# Group Name:   Team Hightower
# Members:      Cori Albritton, Megan Cox, Peter Ford, Timothy Oliver
# Assignment:   CyberStorm Challenge - "Wyly Tower Escape"
# Date:         2 May 2022
# Credit:       Base Room Adventure code is sourced from the Room Adventure Activity in the CSC 131: The Science of Computing II textbook.
#               Timer gui is created based on a modified version of the code found here: https://www.geeksforgeeks.org/create-countdown-timer-using-python-tkinter/
###########################################################################################
import time
from tkinter import *
from tkinter import messagebox
from threading import Thread
from hashlib import md5
from random import randint
import time


DEBUG = False

stop = False

# the floor class
# note that this class is fully implemented with dictionaries as illustrated in the lesson "More on Data Structures"
class Floor(object):
    # the constructor
    def __init__(self, name, image):
        # floors have a name, an image (the name of a file), exits (e.g., south), exit locations
        # (e.g., to the south is floor n), items (e.g., table), item descriptions (for each item),
        # and grabbables (things that can be taken into inventory)
        self.name = name
        self.image = image
        self.exits = {}
        self.items = {}
        self.grabbables = []
        self.openables = []
        self.useables = []
        self.codes = {}
        
    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        self._name = value

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, value):
        self._image = value

    @property
    def exits(self):
        return self._exits

    @exits.setter
    def exits(self, value):
        self._exits = value

    @property
    def items(self):
        return self._items

    @items.setter
    def items(self, value):
        self._items = value

    @property
    def grabbables(self):
        return self._grabbables

    @grabbables.setter
    def grabbables(self, value):
        self._grabbables = value

    @property
    def useables(self):
        return self._useables

    @useables.setter
    def useables(self, value):
        self._useables = value
    
    @property
    def openables(self):
        return self._openables

    @openables.setter
    def openables(self, value):
        self._openables = value

    @property
    def codes(self):
        return self._codes

    @codes.setter
    def codes(self, value):
        self._codes = value
        
    # adds an exit to the floor
    # the exit is a string (e.g., north)
    # the floor is an instance of a floor
    def addExit(self, exit, floor):
        # append the exit and floor to the appropriate dictionary
        self._exits[exit] = floor

    # adds the keyword to change floors
    # the key is a string
    # the floor is an instance of a floor
    def addCode(self, code, floor):
        # append the exit and floor to the appropriate dictionary
        self.codes[code] = floor

    def delCode(self, code):
        # remove the item from the list
        del(self.codes[code])

    # adds an item to the floor
    # the item is a string (e.g., table)
    # the desc is a string that describes the item (e.g., it is made of wood)
    def addItem(self, item, desc):
        # append the item and description to the appropriate dictionary
        self._items[item] = desc

    def delItem(self, item):
        # append the item and description to the appropriate dictionary
        del(self._items[item])

    # adds a grabbable item to the floor
    # the item is a string (e.g., key)
    def addGrabbable(self, item):
        # append the item to the list
        self._grabbables.append(item)
        #if (item in self._items):
         #   self.delGrabbable(item)

    # removes a grabbable item from the floor
    # the item is a string (e.g., key)
    def delGrabbable(self, item):
        # remove the item from the list
        self._grabbables.remove(item)
    
    # adds a useable item to the floor
    # the item is a string (e.g., key)
    def addUseable(self, item):
        # append the item to the list
        self._useables.append(item)

    # removes a useable item from the floor
    # the item is a string (e.g., key)
    def delUseable(self, item):
        # remove the item from the list
        self._useables.remove(item)

    # adds a openable item to the floor
    # the item is a string (e.g., key)
    def addOpenable(self, item):
        # append the item to the list
        self._openables.append(item)

    # removes a openable item from the floor
    # the item is a string (e.g., key)
    def delOpenable(self, item):
        # remove the item from the list
        self._openables.remove(item)

    # returns a string description of the floor
    def __str__(self):
       # first, the floor name
        s = "You are in {}.\n".format(self.name)
       # next, the items in the floor
        s += "You see: "
        for item in self.items.keys():
            s += item + ", "
        s = s[:-2]
        s += "\n"

        s += "Exits: "
        for exit in self.exits.keys():
            s += exit + " "

        return s

################################################################
# the game class
# inherits from the Frame class of Tkinter
class Game(Frame):

    inMinigame = False
    coin = "num"

    # the constructor
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)
        self.goR2 = False
        self.goR3 = False
        self.t1 = None

    # creates the floors
    def createFloors(self):
        # create the floors and give them meaningful names
        r1_e = Floor("Floor 1 Elevator", "Images/e1.gif")
        r1_1 = Floor("Floor 1 Room", "Images/f1r1.gif")

        r2_e = Floor("Floor 2 Elevator", "Images/e2.gif")
        r2_1 = Floor("Floor 2 Room 1", "Images/f2r1.gif")
        r2_2 = Floor ("Floor 2 Room 2", "Images/f2r2.gif")

        r3_e = Floor("Floor 3 Elevator", "Images/e3.gif")
        r3_1 = Floor("Floor 3 Room 1", "Images/f3r1.gif")
        r3_2 = Floor ("Floor 3 Room 2", "Images/f3r2.gif")
        r3_3 = Floor("Floor 3 Room 3", "Images/f3r3.gif")
        
        r4 = Floor("Win", "Images/win.png")

        # add exits to floor 1
        r1_e.addExit("south", r1_1)
        r1_1.addExit("elevator", r1_e)

        # add items to floor 1
        r1_e.addItem("small_sign", "The sign reads 'Don't give up. Recall the blue skies of freedom.'")

        r1_1.addItem("chair", "It is made of wicker and no one is sitting on it.\nThe number |64| is engraved on it.")
        r1_1.addItem("table", "It is made of oak. A golden key and a Game_Board rest on it.")
        r1_1.addItem("caution_sign", "Take it nice and |slow|. Don't lose your life over a foolish accident.\nZzk wtzip s roiw?\nEva ulipazb oarb hgzyo dzcow eck...")
        r1_1.addItem("game_board", "You see an 8x8 game board with chess pieces and Reversi disks on the side.\nThere is an antique gold dollar in the middle.")

        # add grabbables to floor 1
        r1_1.addGrabbable("caution_sign")
        r1_1.addGrabbable("short_note")
        r1_1.addGrabbable("plaque")

        # add (initially allowed) usables to floor 1
        r1_1.addUseable("game_board")
        r1_1.addUseable("keypad")




        # add exits to floor 2
        r2_e.addExit("south", r2_1)
        r2_1.addExit("east", r2_2)
        r2_2.addExit("west", r2_1)
        r2_1.addExit("elevator", r2_e)
        r2_2.addExit("elevator", r2_e)

        # add items to floor 2
        r2_e.addItem("small_sign", "The sign reads 'Don't give up. Recall the blue skies of freedom.'")
        r2_1.addItem("carpet", "It might have been nice at one point but now its just gross and dirty.")
        r2_1.addItem("note", "It reads: On Tech, where is the clock that has stopped?")
        r2_1.addItem("book", "Inside the book there is an odly ciphered piece of text written in the alpabet a-z1-9 asking for a keyword (the exact text should be in your clues folder")
        r2_1.addItem("coffee_table", "A nice coffee table with a note and book sitting on it")
        r2_2.addItem("weird clocktower photo", "Perhaps there is something hidden in this photo of the clocktower. If only you had someThing to get a better look at it. (the photo can be found in the clues folder)")
        r2_2.addItem("rotten orange", "someone needs to clean up around here")
        r2_2.addItem("trash can", "perhaps the rotten orange should go in here")


        # add exits to floor 3
        r3_e.addExit("south", r3_1)

        # key is "oh" -- LINE428 --
        r3_1.addExit("south", r3_2)
        r3_2.addExit("north", r3_1)

        # key is "no" -- LINE432 --
        r3_2.addExit("east", r3_3)
        r3_3.addExit("west", r3_2)
        r3_1.addExit("elevator", r3_e)
        r3_2.addExit("elevator", r3_e)
        r3_3.addExit("elevator", r3_e)

        # add items to floor 3
        r3_e.addItem("small_sign", "The sign reads 'Don't give up. Recall the blue skies of freedom.'")
        r3_1.addItem("banner", "The banner lists all the Tennets of Tech, the \n|KEY| qualities of all Tech students...which is your favorite?")
        r3_1.addItem("sticky_note", "The sticky note says: 'Bwi 7s7wu6si x66 xzw 2ifb 6s64 xw MNLBR alphabet:A-Z0-9'")
        r3_2.addItem("salad", "Gross, its a half eaten |CAESAR| salad...and the reciept says 'H52 82m hc h52 b2lh fcca 6g k52b6bfca2'")
        r3_2.addItem("couch_cushion", "Kinda grimy...and someone wrote in sharpie 'my \n|SHIFT| starts soon, I wonder how many tennets of tech there are?'")
        r3_3.addItem("poster", "Ooh SHAnia Twain! And she signed it saying 'the \nlegend of the bulldog was in which year?'")
        # add grabbables to floor 3
        r1_e.addGrabbable("book")

        # add exit codes to the floors
        r1_1.addCode("854d6fae5ee42911677c739ee1734486",r1_1)
        r1_e.addCode("0684f3d1561cb44c4e88e31530742cc4", r2_e)
        r2_e.addCode("ee0eafb3520cbc3a744bb41656f0a737", r3_e)
        r3_e.addCode("67dbacfcdb2e0c98068a70670301c248",r4)
        r3_1.addCode("c9e8bebd1f410934b634288c41048dc9", r3_2)
        r3_2.addCode("4178e05147e71984321ffeec75a09b52", r3_3)

        # set floor 1 as the current floor at the beginning of the game
        Game.currentFloor = r1_e
        Game.inventory = []  # makes the inventory empty
  # sets up the GUI
    def setupGUI(self):
        self.pack(fill = BOTH, expand = 1)

        #setting up the input region
        Game.player_input = Entry(self, bg = "white")
        Game.player_input.bind("<Return>", self.process)
        Game.player_input.pack(side = BOTTOM, fill = X)
        Game.player_input.focus()

        img = None
        Game.image = Label(self, width= WIDTH//2, image=img)
        Game.image.image = img
        Game.image.pack(side=LEFT, fill=Y)
        Game.image.pack_propagate(False)

        text_frame = Frame(self, width = WIDTH//2)

        Game.text = Text(text_frame, bg= "lightgrey", state = DISABLED)
        Game.text.pack(fill=Y, expand=1)
        text_frame.pack(side=RIGHT, fill=Y)
        text_frame.pack_propagate(False)

  # sets the current floor image
    def setFloorImage(self):
        if (Game.currentFloor == None):
            Game.img = PhotoImage(file = "Images/dead.gif")
        else:
            Game.img = PhotoImage(file = Game.currentFloor.image)

        Game.image.config(image = Game.img)
        Game.image.image = Game.img

  # sets the status displayed on the right of the GUI
    def setStatus(self, status):
        Game.text.config(state = NORMAL)
        Game.text.delete("1.0", END)

        if (Game.currentFloor == None):
            msg = "You died!\n\nUnfortunately, you didn't make it out \nof Wyly Tower before it closed. You tried to\navoid starvation by eating the rotten orange from\nfloor 2 but ended up getting food poisioning\nand dieing! Luckily the Lady of the Mist has\ndecided to bring you back and give you\nanother chance!\n\nGo ahead and close the game and give it\nanother try!"
            Game.text.insert(END, msg)
        else:
                Game.text.insert(END, str(Game.currentFloor) +\
                                 "\nYou are carrying: "+ str(Game.inventory) +\
                                 "\n\n" + status)

        Game.text.config(state = DISABLED)

  # plays the game
    def play(self):
        # add the floors to the game
        self.createFloors()
        # configure the GUI
        self.setupGUI()
        # set the current floor
        self.setFloorImage()
        # set the current status
        self.setStatus("")

    def timerGUI():
        global stop
        # creating Tk window
        root = Toplevel()

        # setting geometry of tk window
        root.geometry("300x100")
        root.overrideredirect(True)
        
        # Declaration of variables
        minute=StringVar()
        second=StringVar()
        
        # setting the default value as 0 and create labels
        # timer currently set to 01:30
        minute.set("05")
        second.set("00")
        minuteLabel = Label(root, textvariable=minute, font = ("Arial", 32)) 
        minuteLabel.place(x=80,y=20)
        secondLabel = Label(root, textvariable=second, font = ("Arial", 32)) 
        secondLabel.place(x=130,y=20)

        try:
            # the input provided by the user is
            # stored in here :temp
            temp = int(minute.get())*60 + int(second.get())
        except:
            print("Please input the right value")
        while temp >-1:
                
            # divmod(firstvalue = temp//60, secondvalue = temp%60)
            mins,secs = divmod(temp,60)

            # Converting the input entered in mins or secs to hours,
            # mins ,secs(input = 110 min --> 120*60 = 6600 => 1hr :
            # 50min: 0sec)
            if mins >60:
                    
                # divmod(firstvalue = temp//60, secondvalue
                # = temp%60)
                mins = divmod(mins, 60)
                
            # using format () method to store the value up to
            # two decimal places
            minute.set("{0:2d}".format(mins))
            second.set("{0:2d}".format(secs))

            # updating the GUI window after decrementing the
            # temp value every time
            root.update()
            time.sleep(1)

            # when temp value = 0; then a messagebox pop's up
            # with a message:"Time's up"
            if (temp == 0):
                root.destroy()

            if (stop):
                root.destroy()
                
            # after every one sec the value of temp will be decremented
            # by one
            temp -= 1

    def timerThread(self):
        self.t1 = Thread(target=Game.timerGUI)
        self.t1.start()

    # for non-floor traversing codes
    def specialCodeAct(self, floor, code):
        msg = 'WRONG CODE'
        # should replace with hashed password codes later
        if code == "854d6fae5ee42911677c739ee1734486":
            floor.delUseable("keypad")
            floor.addItem("keypad_hint", "The solved keypad reads 'W?W?W???W??WW?W?WW?WWWWWW??WW??WW??W????W??W??WWW??W??WWW??W????W???W???WW?WWWWWW??W?WW?W??W???WWW?WWWWWW???W?WWW??W?WWWW??WW?W?WW?WWWWWW??WW??WW??W????W??W????W???W?WWW???WW??W???W?WWW??WW?W?W???WWWWW???WW??WW?WWWWWW??W????W??WW??WWW?WWWWWW??W????W???W?W?W???WW?WWW?WWWWWW??W???WW??W????W???W?W?W???WW?WW??W?WW?W???WW??W??W?WWWW??W?WW?W??W???WW??WW???WW?WWWWWW??W??W?W??W????W???W?WWW??W?WWWW??WW?W?W???WW?WWW?WW???W???WW??WW?WWWWWW??WW??WW??W?WW?W???WW?WW???WW??W???W?WWWW?WWWWWW??WWW?WW??WWWW?W??WWW?WW????WW?WW?WWWWWW??WWW?WW??W?WW?W???WW?WW??WW?WWWW?WWWWWW???W???W??W?WWWW??W????WW?WWWWWW??WW??WW??W??WWW??WW?W?W???W???WW?WWWWWW???W?WWW??W?WWWW??WW?W?WW?WWWWWW??W???WW??WW?W?W???WW??W???W?WWWW?WWWWWW??W?WW?W??W???WWW?WWWWWW?WW??W?W?WWW?WWW?WWWW??W?WWWW??W?WWWW??W?W??WWWW?WWWW??W?W?W??WW?WW?WW?W?WW?WW?WW?W???W'\n")

            floor.addItem("keypad_hint2","W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W??")
            floor.addItem("keypad_hint3","?WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W??")
            floor.addItem("keypad_hint4","??W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?W?W??W?WW??WW?W?W???WW?WW??W????W?WW????W??W???WW??WW?W?W?WW????W??W???WW??WW?W?")
            floor.delCode(code)
            msg = "Great job on using the 'enter' command. You'll be using it a lot more.\nLook for some new items or a *plaque*."
        elif code == "c9e8bebd1f410934b634288c41048dc9":
            self.goR2 = True
            msg = "The door unlocked!"
        elif code == "4178e05147e71984321ffeec75a09b52":
            self.goR3 = True
            msg = "The door unlocked!"
        return msg

    def useItem(noun):
        if (noun == "short_note"):
            return "The short_note reads . . .\n"+\
                   "Dr. Guice just had to have a chess board in this room. Something "+\
                   "about the number of tiles, I think.\n\n"+\
                   "A small stamp depicting the Roman Colosseum is in the bottom corner with 'Tai ymzk efgpqzfe qzdaxxqp mf Fqot itqz uf ime rudef ragzpqp' written across it."
        if (noun == "plaque"):
            return "The plaque reads . . .\n"+\
                   "Here's an easy hint as a reward\n"+\
                   "The password to the next floor is the name of our university's first graduate.\n"+\
                   "Think of the auditorium in the Quad.\n"+\
                   "His first and last name with no spaces. Type 'enter <password>' in the elevator to try."
        else:
            return "That item doesn't look like it can be used here."

    def coinflip(n, mustWin):
        wins = 0

        for j in range(n):
            if (randint(0,1)):
                wins+=1

        if wins >= mustWin:
            return True
        return False
    
    def useStatic(self, floor, noun):
        tosses = randint(3,7)
        mustWin = tosses//2+1
        response = ""
        
        if (floor.name == "Floor 1 Room"):
            if noun == "game_board":
                response += f"You played a round of coin flips with {tosses} tosses.\n"+\
                            f"To win and get the prize, you need to call {mustWin} correctly.\n"
                if(Game.coinflip(tosses, mustWin)):
                    floor.addGrabbable("short_note")
                    response += "\nYou won!\n\nThe board parts down the middle and a *short_note* floats up beckoning you to *take* it."
                else:
                    response += "\nYou lost :(\n\nLooks like you'll have to try again."


            elif noun == "keypad":
                response+= "The keypad lights up and reads 'Please `enter` the password'."

            return response

    def checkItemToTake(floor,noun):
        if (noun == "caution_sign"):
            floor.addItem("sticky_note", "It reads 'There's this odd *keypad* underneath the table'.")
            floor.addItem("keypad", "It lightly shines waiting for you to enter a code.")


  # processes the player's input
    def process(self, event):
        action = Game.player_input.get()
        action = action.lower()
        f3 = ("Floor 3 Elevator", "Floor 3 Room 1", "Floor 3 Room 2", "Floor 3 Room 3")
        response = "I don't understand. Try verb or noun. Valid verbs are go, look, take, open, use, or enter."
        global stop

        if (action == "quit" or action == "bye"):
            exit(0)

        if (Game.currentFloor == None):
            Game.player_input.delete(0, END)
            return

        if (Game.currentFloor.name in f3):
            if self.t1.is_alive():
                pass
            else:
                Game.currentFloor = None
                action = ""
                response = ""

        words = action.split()
        if (len(words) == 2):
            verb = words[0]
            noun = words[1]

            if (verb == "go"):
                response = "INVALID EXIT"
                if (noun in Game.currentFloor.exits):
                    if ((Game.currentFloor.name == "Floor 3 Room 1")):
                        if self.goR2 or not(noun == "south"):
                            Game.currentFloor = Game.currentFloor.exits[noun]
                            response = "Room Changed"
                        else:
                            response = "The door is locked, and you can't open it."
                    elif Game.currentFloor.name == "Floor 3 Room 2":
                        if self.goR3 or not(noun == "east"):
                            Game.currentFloor = Game.currentFloor.exits[noun]
                            response = "Room Changed"
                        else:
                            response = "The door is locked, and you can't open it."
                    else:
                        Game.currentFloor = Game.currentFloor.exits[noun]
                        response = "Room Changed"

            if ((DEBUG) and verb == "codes"):
                response = ''
                for val in Game.currentFloor.codes:
                    response += f"{val}\n"

            if (verb == "enter"):
                response = "WRONG CODE"
                code = str(md5(noun.encode('UTF-7')).hexdigest())
                if (code in Game.currentFloor.codes):

                    # for extra codes that don't transfer you to a new floor


                    if ("Elevator" not in Game.currentFloor.name):
                        response = self.specialCodeAct(Game.currentFloor, code)
                    else:
                        Game.currentFloor = Game.currentFloor.codes[code]
                        if (Game.currentFloor.name == "Win"):
                            response = "Congratulations! \n\nYou managed to escape Wyly Tower and are greeted\nby a group applauding you effort and Tech XXII.\nYou are rewarded by getting the chance to give\nTech XXII some pets. What a treat!\n\nYou've completed The Great Wyly Escape challenge and can now claim your points."
                            stop = True
                        else:
                            response = "You got it! Moved to next challenge floor.\nYou dropped everything you obtained on this floor in the void."
                        if (Game.currentFloor.name == "Floor 3 Elevator"):
                            response = response + "\n\n" + "Uh oh! There's only 5 minutes left until Wyly\nTower closes! \nIf you don't get the last code in time, you'll be stuck inside for who knows how long. \nBetter hurry!"
                            Game.timerThread(self)
                        Game.inventory = []


            elif (verb == "look"):
                response = "I don't see anything"

                if (noun in Game.currentFloor.items):
                    response = Game.currentFloor.items[noun]

            elif (verb == "take"):
                response = "I can't take anything"

                if noun in Game.currentFloor.grabbables:
                    Game.inventory.append(noun)
                    Game.currentFloor.delGrabbable(noun)
                    if noun in Game.currentFloor.items:
                        Game.checkItemToTake(Game.currentFloor,noun)
                        Game.currentFloor.delItem(noun)

                    response = "Item Grabbed"
                    if noun == "caution_sign":
                        response += "\nThere was a sticky_note underneath."

            elif(verb == "use"):
                # default respone
                response = "That item doesn't look like it can be used here."
                if (noun in Game.inventory):
                    response = Game.useItem(noun)
                elif (noun in Game.currentFloor.useables):
                    response = self.useStatic(Game.currentFloor, noun)

            elif (verb == "open"):
                # default response
                response = "That can't be opened."

        self.setStatus(response)
        self.setFloorImage()

        Game.player_input.delete(0, END)

##########################################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600

# create the window
window = Tk()
window.title("The Great Wyly Tower Escape")

# create the GUI as a Tkinter canvas inside the window
g = Game(window)
# play the game
g.play()

# wait for the window to close
window.mainloop()
