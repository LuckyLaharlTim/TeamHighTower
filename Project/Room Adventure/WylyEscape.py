###########################################################################################
# Name: Megan Cox
# Date: 4/10/19
# Description: floor Adventure
###########################################################################################
import time
from tkinter import *
from tkinter import messagebox
from threading import Thread


DEBUG = True

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

    # adds an item to the floor
    # the item is a string (e.g., table)
    # the desc is a string that describes the item (e.g., it is made of wood)
    def addItem(self, item, desc):
        # append the item and description to the appropriate dictionary
        self._items[item] = desc

    # adds a grabbable item to the floor
    # the item is a string (e.g., key)
    def addGrabbable(self, item):
        # append the item to the list
        self._grabbables.append(item)
        if (item in self._items):
            self.delGrabbable(item)

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
    # the constructor
    def __init__(self, parent):
        # call the constructor in the superclass
        Frame.__init__(self, parent)
        self.t1 = None

    # creates the floors
    def createFloors(self):
        # create the floors and give them meaningful names
        r1_e = Floor("Floor 1 Elevator", "room1.gif")
        r1_1 = Floor("Floor 1 Room", "room1.gif")

        r2_e = Floor("Floor 2 Elevator", "room2.gif")
        r2_1 = Floor("Floor 2 Room 1", "room2.gif")
        r2_2 = Floor ("Floor 2 Room 2", "room2.gif")

        r3_e = Floor("Floor 3 Elevator", "room3.gif")
        r3_1 = Floor("Floor 3 Room 1", "room3.gif")
        r3_2 = Floor ("Floor 3 Room 2", "room3.gif")
        r3_3 = Floor("Floor 3 Room 3", "room3.gif")
        
        r4 = Floor("Finish", "room4.gif")

        # add exits to floor 1
        r1_e.addExit("south", r1_1)
        r1_1.addExit("elevator", r1_e)

        # add items to floor 1
        r1_e.addItem("small_sign", "The sign reads 'Don't give up. Recall the blue skies of freedom.'")
        
        r1_1.addItem("chair", "It is made of wicker and no one is sitting on it.\nThe number 64 is engraved on it.")
        r1_1.addItem("table", "It is made of oak. A golden key and a Game_Board rest on it.")
        r1_1.addItem("caution_sign", "Take it nice and |slow|. Don't lose your life over a foolish accident.\nZzk wtzip s roiw zt Nwgsnkt?")
        r1_1.addItem("Game_Board", "You see an 8x8 game board with chess pieces and Reversi disks on the side.\nYou feel like there's an opponent nearby despite being alone.")

        # add grabbables to floor 1
        r1_1.addGrabbable("caution_sign")
        r1_1.addGrabbable("short_note") 
        r1_1.addGrabbable("plaque")

        # add (initially allowed) usables to floor 1
        r1_1.addUseable("Game_Board")
        r1_1.addUseable("keypad")
        print(f"floor 1 room 1 useables: {r1_1.useables}")
       
        

        # add exits to floor 2
        r2_e.addExit("south", r2_1)
        r2_1.addExit("east", r2_2)
        r2_2.addExit("west", r2_1)
        r2_1.addExit("elevator", r2_e)
        r2_2.addExit("elevator", r2_e)

        # add items to floor 2
        r2_e.addItem("small_sign", "The sign reads 'Don't give up. Recall the blue skies of freedom.'")
        r2_1.addItem("rug", "It is nice and Indian. It also needs to be vacuumed.")
        r2_1.addItem("fireplace", "It is full of ashes.")
        r2_1.addItem("note", "It reads: On Tech, where is the clock that has stopped?")
        r2_1.addItem("book", "inside the book there is an odly ciphered piece of text written in the alpabet a-z1-9 asking for a keyword (the exact text should be in your folder")
        r2_1.addItem("desk", "A nice mahogany desk with a note sitting on it")
        r2_2.addItem("wierd cloocktower photo", "Perhaps there is something hidden in this photo of the clocktower (the photo should be in your directory)")
        r2_2.addItem("rotten orange", "someone needs to clean up around here")
        r2_2.addItem("trash can", "perhaps the rotten orange should go in here")
        
        # add exits to floor 3
        r3_e.addExit("south", r3_1)
        r3_1.addExit("south", r3_2)
        r3_2.addExit("north", r3_1)
        r3_2.addExit("east", r3_3)
        r3_3.addExit("west", r3_2)
        r3_1.addExit("elevator", r3_e)
        r3_2.addExit("elevator", r3_e)
        r3_3.addExit("elevator", r3_e)

        # add items to floor 3
        r3_e.addItem("small_sign", "The sign reads 'Don't give up. Recall the blue skies of freedom.'")
        
        # add grabbables to floor 3
        r1_e.addGrabbable("book")

        # add exit codes to the floors
        r1_1.addCode("u(7;q9#my_5;pjny",r1_1)
        r1_e.addCode("harryhoward", r2_e)
        r2_e.addCode("11:05", r3_e)
        r3_e.addCode("key3",r4)

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
            Game.img = PhotoImage(file = "skull.gif")
        else:
            Game.img = PhotoImage(file = Game.currentFloor.image)

        Game.image.config(image = Game.img)
        Game.image.image = Game.img

  # sets the status displayed on the right of the GUI
    def setStatus(self, status):
        Game.text.config(state = NORMAL)
        Game.text.delete("1.0", END)

        if (Game.currentFloor == None):
                Game.text.insert(END, "You died!")
        else:
                Game.text.insert(END, str(Game.currentFloor) +\
                                 "\n You are carrying: "+ str(Game.inventory) +\
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
        # creating Tk window
        root = Toplevel()

        # setting geometry of tk window
        root.geometry("300x100")
        root.overrideredirect(True)
        
        # Declaration of variables
        hour=StringVar()
        minute=StringVar()
        second=StringVar()
        
        # setting the default value as 0 and create labels
        # timer currently set to 01:30
        minute.set("01")
        second.set("30")
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
                
            # after every one sec the value of temp will be decremented
            # by one
            temp -= 1

    def timerThread(self):
        self.t1 = Thread(target=Game.timerGUI)
        self.t1.start()

    # for non-floor traversing codes
    def specialCodeAct(floor, code):
        # should replace with hashed password codes later
        if code == "u(7;q9#my_5;pjny":
            floor.delUseable("keypad")
            floor.addItem("keypad_hint", "The solved keypad reads 'HarryHoward in word form binary'")
            return "Great job on using the 'enter' command. You'll be using it a lot more.\nHere's your payload:\nHarryHoward in word form binary" 
            

  # processes the player's input
    def process(self, event):
        action = Game.player_input.get()
        action = action.lower()
        f3 = ("Floor 3 Elevator", "Floor 3 Room 1", "Floor 3 Room 2", "Floor 3 Room 3")
        response = "I don't understand. Try verb or noun. Valid verbs are go, look, take, open, use, or enter."

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

        words = action.split()
        if (len(words) == 2):
            verb = words[0]
            noun = words[1]

            if (verb == "go"):
                response = "INVALID EXIT"
                if (noun in Game.currentFloor.exits):
                    Game.currentFloor = Game.currentFloor.exits[noun]
                    response = "Room Changed"

            if ((DEBUG) and verb == "codes"):
                response = ''
                for val in Game.currentFloor.codes:
                    response += f"{val}\n"

            if (verb == "enter"):
                response = "WRONG CODE"
                    
                if (noun in Game.currentFloor.codes):
                    # for extra codes that don't transfer you to a new floor
                    #print(f"response was . . .\n{response}")
                    
                    if ("Elevator" not in Game.currentFloor.name):
                        #print(f"wasn't in elevator\tcurrently in {Game.currentFloor.name}\noutput should be: {Game.specialCodeAct(Game.currentFloor, noun)}")
                        response = Game.specialCodeAct(Game.currentFloor, noun)
                    else:
                        Game.currentFloor = Game.currentFloor.codes[noun]
                        response = "You got it! Moved to next challenge floor."
                        #print(f"was in elevator\tcurrently in {Game.currentFloor.name}\noutput should be: {response}")
                        if (Game.currentFloor.name == "Floor 3 Elevator"):
                            response = response + "\n" + "Timer started"
                            Game.timerThread(self)
                #print(f"response is now . . .\n{response}")

            elif (verb == "look"):
                response = "I don't see anything"

                if (noun in Game.currentFloor.items):
                    response = Game.currentFloor.items[noun]

            elif (verb == "take"):
                response = "I can't take anything"

                for grabbable in Game.currentFloor.grabbables:
                    if (noun == grabbable):
                        Game.inventory.append(grabbable)
                        Game.currentFloor.delGrabbable(grabbable)

                        response = "Item Grabbed"
                        break
            elif(verb == "use"):
                # default respone
                response = "That item doesn't look like it can be used here."
            
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
window.title("Extreme Wyly Tower Escape")

# create the GUI as a Tkinter canvas inside the window
g = Game(window)
# play the game
g.play()

# wait for the window to close
window.mainloop()
