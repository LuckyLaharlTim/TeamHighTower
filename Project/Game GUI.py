#################################################################
# Name:Peter Ford
# Date:
# Description:
#################################################################
from Tkinter import *
# the room class
death = "skull.gif"
class Room(object):
        # the constructor
    def __init__(self, name, image):
        # rooms have a name, an image (the name of a file),
        # exits (e.g., south), exit locations
        # (e.g., to the south is room n), items (e.g., table),
        # item descriptions (for each item), and grabbables
        # (things that can be taken into inventory)
        self.name = name
        self.image = image
        self.exits = {}
        self.items = {}
        self.item_key = []
        self.grabbables = []


# getters and setters for the instance variables
    @property
    def name(self):
        return self._name
    @name.setter
    def name(self, value):
        self._name = value
 #getter and setters for old lists       
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
    def item_key(self):
        return self._item_key
    @item_key.setter
    def item_key(self, value):
        self._item_key = value
        
    @property
    def grabbables(self):
        return self._grabbables
    @grabbables.setter
    def grabbables(self, value):
        self._grabbables = value
    @property
    def image(self):
        return self._image
    @image.setter
    def image(self, value):
        self._image = value

# adds an exit to the room
    # the exit is a string (e.g., north)
    # the room is an instance of a room
    
    def addExit(self, exit, room):
        # append the exit and room to the appropriate dictonary
        self._exits[exit] = room

 # adds an item to the room
    # the item is a string (e.g., table)
    # the desc is a string that describes the item (e.g., it is made
    # of wood)
    def addItem(self, item, desc, key = None):
        # append the item and exit to the appropriate lists and dictionary
        self._items[item] = desc
        self._item_key.append(key)
        
    def delItem(self, item, desc, key = None):
        # remove the item from the list
        del self._items[item]
        self._item_key.remove(key)
        
    # adds a grabbable item to the room
    # the item is a string (e.g., key)
    def addGrabbable(self, item):
        # append the item to the list
        self._grabbables.append(item)
        
    # removes a grabbable item from the room
    # the item is a string (e.g., key)
    def delGrabbable(self, item):
        # remove the item from the list
        self._grabbables.remove(item)

     # returns a string description of the room
    def __str__(self):
        # first, the room name
        s = "You are in {}.\n".format(self.name)
        # next, the items in the room
        s += "You see: "
        for item in self.items.keys():
            s += item + " "
        s += "\n"
        # next, the exits from the room
        s += "Exits: "
        for exit in self.exits.keys():
            s += exit + " "
        s = s.replace(r'\n', '\n')
        return s
    #win function
    def win():
            print "Congratulations, you beat my game!"
            print "\nCredits: Peter Ford"
            print "\n1/7/2019"
            print "LaTech outline with creative liberties added"

class Game(Frame):
    #constructor
    def __init__(self,parent):
        #call the constructor in superclass
        Frame.__init__(self, parent)

  
    #creat rooms
    def createRooms(self):
        # r1 through r4 are the four rooms in the mansion
        # currentRoom is the room the player is currently in (which
        # can be one of r1 through r4)
        # create the rooms and give them meaningful names and an
        # image in the current directory
        self.r1 = Room("Room 1", "room1.1.gif")
        self.r2 = Room("Room 2", "room2.1.gif")
        r3 = Room("Room 3", "room3.1.gif")
        r4 = Room("Room 4", "room4.1.gif")
        self.r5 = Room("attic", "attic.gif")
        self.r6 = Room("outside", "outside.gif")
        
        # add exits to room 1
        self.r1.addExit("east", self.r2) # to the east of room 1 is room 2
        self.r1.addExit("south", r3)
        # add grabbables to room 1
        self.r1.addGrabbable("key")
        # add items to room 1
        self.r1.addItem("chair", "It is made of wicker and no one is sitting on it.")
        self.r1.addItem("table", "It is made of oak. A golden *key* rests on it.")
        self.r1.addItem("door", "It appears to be jammed shut beyond hope", "crowbar")
        
        # add exits to room 2
        self.r2.addExit("west", self.r1)
        self.r2.addExit("south", r4)
        self.r2.addExit("attic", self.r5)
        # add items to room 2
        self.r2.addItem("rug", "It is nice and Indian. It also needs to be vacuumed.")
        self.r2.addItem("fireplace", "It is full of ashes.")
        
        # add exits to room 3
        r3.addExit("north", self.r1)
        r3.addExit("east", r4)
        # add grabbables to room 3
        r3.addGrabbable("book")
        # add items to room 3
        r3.addItem("bookshelves", "They are empty. Go figure.")
        r3.addItem("statue", "There is nothing special about it.")
        r3.addItem("desk", "The statue is resting on it. So is a *book*.")
        
        # add exits to room 4
        r4.addExit("north", self.r2)
        r4.addExit("west", r3)
        r4.addExit("south", None) # DEATH!
        # add grabbables to room 4
        r4.addGrabbable("6-pack")
        # add items to room 4
        r4.addItem("brew_rig", "Gourd is brewing some sort of oatmeal stout on the brew rig. A *6-pack* is resting beside it.")

        #add exits to room 5
        self.r5.addExit("down", self.r2)
        #add items to r5
        self.r5.addItem("old_toys", "It looks like Gourd has a couple of his childhood toys stashed up here.")
        self.r5.addItem("window", "An ancient looking single pane window with a basic latch")
        self.r5.addItem("chest", "A dusty chest with a huge padlock dangling off the front", "key")

        # set room 1 as the current room at the beginning of the
        # game
        Game.currentRoom = self.r1
        # initialize the player's inventory
        Game.inventory = []

    def openChest(self):
        self.r5.image = "attic.1.gif"

##        self.r7 = Room("attic","attic.1.gif")
##         #add exits to room 5
##        self.r7.addExit("down", self.r2)
##        #add items to r5
##        self.r7.addItem("old_toys", "It looks like Gourd has a couple of his childhood toys stashed up here.")
##        self.r7.addItem("window", "An ancient looking single pane window with a basic latch")
##        self.r7.addItem("opened_chest", "A slightly rusted *crowbar* lies inside.")
##        Game.currentRoom = self.r7


    def create_End(self):
        self.r1.image = "room1.2.gif"
        self.r1.addExit("door", self.r6)
        
    
    
    #setup GUI
    def setupGUI(self):
        # organize the GUI
        self.pack(fill=BOTH, expand=1)
        # setup the player input at the bottom of the GUI
        # the widget is a Tkinter Entry
        # set its background to white and bind the return key to the
        # function process in the class
        # push it to the bottom of the GUI and let it fill
        # horizontally
        # give it focus so the player doesn't have to click on it
        Game.player_input = Entry(self, bg="white")
        Game.player_input.bind("<Return>", self.process)
        Game.player_input.pack(side=BOTTOM, fill=X)
        Game.player_input.focus()
        # setup the image to the left of the GUI
        # the widget is a Tkinter Label
        # don't let the image control the widget's size
        img = None
        Game.image = Label(self, width=WIDTH / 2, image=img)
        Game.image.image = img
        Game.image.pack(side=LEFT, fill=Y)
        Game.image.pack_propagate(False)
        # setup the text to the right of the GUI
        # first, the frame in which the text will be placed
        text_frame = Frame(self, width=WIDTH / 2)
        # the widget is a Tkinter Text
        # disable it by default
        # don't let the widget control the frame's size
        Game.text = Text(text_frame, bg="lightgrey", state=DISABLED)
        Game.text.pack(fill=Y, expand=1)
        text_frame.pack(side=RIGHT, fill=Y)
        text_frame.pack_propagate(False)

    #set up current image
    def setRoomImage(self):
        if (Game.currentRoom == None):
            
            # if dead, set the skull image
            Game.img = PhotoImage(file="skull.gif")
            #print "it made it here"
        else:
            #Game.currentRoom.image
            # otherwise grab the image for the current room
            Game.img = PhotoImage(file=Game.currentRoom.image)
            # display the image on the left of the GUI
        Game.image.config(image=Game.img)
        Game.image.image = Game.img
    #sets status on right of GUI
    def setStatus(self,status):
        # enable the text widget, clear it, set it, and disabled it
        Game.text.config(state=NORMAL)
        Game.text.delete("1.0", END)
        if (Game.currentRoom == None):
            # if dead, let the player know
            Game.text.insert(END, "You are dead. The only thing you can do now is   quit.\n")
        else:
            help_me = "\n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n \n  \n \n \n \n \n \ntype 'help me' to get a list of commands"
            # otherwise, display the appropriate status
            Game.text.insert(END, str(Game.currentRoom) +\
            "\nYou are carrying: " + str(Game.inventory) +\
            "\n\n" + status+ str(help_me))
            Game.text.config(state=DISABLED)
    #play
    def play(self):
        self.createRooms()
        self.setupGUI()
        self.setRoomImage()
        self.setStatus("")

    #process player input
    def process(self,event):
        # grab the player's input from the input at the bottom of
        # the GUI
        action = Game.player_input.get()
        # set the user's input to lowercase to make it easier to
        # compare the verb and noun to known values
        action = action.lower()
        # set a default response
        response = "I don't understand. Try verb noun. Valid verbs are go, look, and take"
        # exit the game if the player wants to leave (supports quit,
        # exit, and bye)
        if (action == "quit" or action == "exit" or action == "bye" or action == "sionara!"):
            exit(0)


        # if the player is dead if goes/went south from room 4
        if (Game.currentRoom == None):
            # clear the player's input
            Game.player_input.delete(0, END)
            return

        # split the user input into words (words are separated by
        # spaces) and store the words in a list
        words = action.split()
        # the game only understands two word inputs
        if (len(words) == 2):
            # isolate the verb and noun
            verb = words[0]
            noun = words[1]

            # the verb is: go
            if (verb == "go"):
                # set a default response
                response = "Invalid exit."
                # check for valid exits in the current room
                if (noun in Game.currentRoom.exits):

                    # if one is found, change the current room to
                    # the one that is associated with the
                    # specified exit
                    Game.currentRoom = Game.currentRoom.exits[noun]
                    # set the response (success)
                    response = "Room changed."

            # the verb is: look
            elif (verb == "look"):
                # set a default response
                response = "I don't see that item."
                # check for valid items in the current room
                if (noun in Game.currentRoom.items):
                    # if one is found, set the response to the
                    # item's description
                    response = Game.currentRoom.items[noun]

            # the verb is: take
            elif (verb == "take"):
                # set a default response
                response = "I don't see that item."
                # check for valid grabbable items in the current
                # room
                for grabbable in Game.currentRoom.grabbables:
                    # a valid grabbable item is found
                    if (noun == grabbable):
                        # add the grabbable item to the player's
                        # inventory
                        Game.inventory.append(grabbable)
                        # remove the grabbable item from the
                        # room
                        Game.currentRoom.delGrabbable(grabbable)
                        # set the response (success)
                        response = "Item grabbed."
                        # no need to check any more grabbable
                        # items
                        break
            elif(verb == "help"):
                response = "the commands are 'go', 'look', use, and 'take'"+"\nGo supports directions e.g. go north, go south, go east, go west"+"\nLook and Take depend on items in the game e.g. look table, take key"+"\nUse depends on items in the game and may require certain items to be in your \ninventory e.g. use window (hint: 3 items can be 'used')" 

            elif(verb == "use"):
                #default respone
                response = "That item doesn't look like it can be used here."
                #chescks for room
                if(Game.currentRoom.name == "attic"):
                    if(noun == "window"):
                        #sucess response
                        response = "Good Job, now ther is shattered glass all over"
                        Game.currentRoom.delItem("window", "An ancient looking single pane window with a basic latch")
                        Game.currentRoom.addItem("broken_window", "A broken window with vicious glass shards surrounding it")
                    elif(noun == "chest"):
                        #finds index for the item_key
                        for i in range(len(Game.currentRoom.items)):
                            #print "found key index"
                            #print currentRoom.items.keys()
                            if(noun in Game.currentRoom.items.keys()):
                                #print "found chest but no response change"
                                for things in Game.inventory:
                                    
                                    #if you have the key in your invetory you can open it
                                    if(things == Game.currentRoom.item_key[i]):
                                        response = "You unlock the padlock and open the chest."
                                        Game.inventory.remove("key")
                                        Game.currentRoom.delItem("chest", "A dusty chest with a huge padlock dangling off the front", "key")
                                        Game.currentRoom.addItem("opened_chest", "A slightly rusted *crowbar* lies inside.")
                                        Game.currentRoom.addGrabbable("crowbar")
                                        self.openChest()
                elif(Game.currentRoom.name == "Room 1"):
                    #print"in room 1"
                    if(noun == "door"):
                        #print "found door"
                        #finds index for the item_key
                        for i in range(len(Game.currentRoom.items)):
                            #print "searching index- " + str(i)
                            if(noun in Game.currentRoom.items.keys()):
                                for things in Game.inventory:
                                    #print "missing key"
                                    #if you have the key in your invetory you can open it
                                    if (things == Game.currentRoom.item_key[i]):
                                        response = "You open the door and look upon the open world."
                                        Game.create_End(self)
                                    

        
                        
                
        # display the response on the right of the GUI
        # display the room's image on the left of the GUI
        # clear the player's input
        self.setRoomImage()
        self.setStatus(response)
        
        Game.player_input.delete(0, END)
                    
                                        


##########################################################
# the default size of the GUI is 800x600
WIDTH = 800
HEIGHT = 600
# create the window
window = Tk()
window.title("Room Adventure")
# create the GUI as a Tkinter canvas inside the window
g = Game(window)
# play the game
g.play()
# wait for the window to close
window.mainloop()
