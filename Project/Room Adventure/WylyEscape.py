###########################################################################################
# Name: Megan Cox
# Date: 4/10/19
# Description: floor Adventure
###########################################################################################
from Tkinter import *

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

  # adds an exit to the floor
  # the exit is a string (e.g., north)
  # the floor is an instance of a floor
    def addExit(self, exit, floor):
        # append the exit and floor to the appropriate dictionary
        self._exits[exit] = floor

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

  # removes a grabbable item from the floor
  # the item is a string (e.g., key)
    def delGrabbable(self, item):
        # remove the item from the list
        self._grabbables.remove(item)

  # returns a string description of the floor
    def __str__(self):
       # first, the floor name
       s = "You are in {}.\n".format(self.name)
       # next, the items in the floor
       s += "You see: "
       for item in self.items.keys():
           s += item + " "
           s += "\n"

       #next, the grabbables
           s += "There is: "
       for grabbable in self.grabbables:
           s += grabbable + " "
           s += "\n"

        # next, the exits from the floor
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

    # creates the floors
    def createFloors(self):
        # create the floors and give them meaningful names
        r1 = Floor("Floor 1", "room1.gif")
        r2 = Floor("Floor 2", "room2.gif")
        r3 = Floor("Floor 3", "room3.gif")
        r4 = Floor("Finish", "room4.gif")

        # add exits to floor 1
        r1.addExit("key1", r2) # -> to the east of floor 1 is floor 2

        # add items to floor 1
        r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
        r1.addItem("table", "It is made of oak. A golden key rests on it.")

        # add exits to floor 2
        r2.addExit("key2", r3)

        # add items to floor 2
        r2.addItem("rug", "It is nice and Indian. It also needs to be vacuumed.")
        r2.addItem("fireplace", "It is full of ashes.")

        # add exits to floor 3
        r3.addExit("key3", r4)

        # add grabbables to floor 3
        r3.addGrabbable("book")

        # set floor 1 as the current floor at the beginning of the game
        Game.currentFloor = r1
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
        Game.image = Label(self, width= WIDTH/2, image=img)
        Game.image.image = img
        Game.image.pack(side=LEFT, fill=Y)
        Game.image.pack_propagate(False)

        text_frame = Frame(self, width = WIDTH/2)

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

  # processes the player's input
    def process(self, event):
        action = Game.player_input.get()
        action = action.lower()
        response = "I don't understand. Try very or noun. Valid verbs are go, look, snd take"

        if (action == "quit" or action == "bye"):
            exit(0)

        if (Game.currentFloor == None):
            game.player_input.delete(0, END)
            return

        words = action.split()
        if (len(words) == 2):
            verb = words[0]
            noun = words[1]

            if (verb == "go"):
                response = "INVALID EXIT"

                if (noun in Game.currentFloor.exits):
                    Game.currentFloor = Game.currentFloor.exits[noun]
                    response = "Floor Changed"

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
