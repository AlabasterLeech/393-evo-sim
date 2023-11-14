"""This module contains the classes which define the GUI.

"""
#Import statements
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from functools import partial
import os

#Module level constant definitions.
_WINDOW_TITLE = "Cellvolution 1.0"
_MIN_WIN_WIDTH = 640
_MIN_WIN_HEIGHT = 480
_MAX_ENV_WIDTH = 1000
_MIN_ENV_WIDTH = 10
_MAX_ENV_HEIGHT = 1000
_MIN_ENV_HEIGHT = 10


class gameWindow(tk.Tk):
    """A gameWindow is an extenstion of a tkinter root which initializes with the ttk frames needed
    for cellvolution. Other than what it inherits, gameWindow has methods which:
    Clear the window (clearWindow)
    Change its state to each of its menus/displays
    Get the file path for a save to load
    """
    def __init__(self):
        tk.Tk.__init__(self)
        self.title(_WINDOW_TITLE)
        self.minsize(_MIN_WIN_WIDTH,_MIN_WIN_HEIGHT)
        self.mainMenu = mainFrame(self)
        self.tutMenu = tutorialFrame(self)
        self.newSimMenu = newSimFrame(self)
        self.simFilePath = None
        

    """Method to forget everything currently being displayed in the game window.
    IMPORTANT: This does not deallocate the memory for the frames/widgets which means they can be reused
    but also means they should not be recreated as this could lead to memory leakage."""
    def clearWindow(self):
        for widget in self.winfo_children():
            widget.pack_forget()

    """Uses a tkinter filedialog to get the path to a JSON file the user would like to load, which can then be passed to the function which
    will actually parse from the JSON file and initialize the simulation state."""
    def getFilePath(self, *options):
        self.simFilePath = filedialog.askopenfilename(parent = self, filetypes=[("JSON Files", "*.json")])

    def changeToMainMenu(self):
        self.clearWindow()
        self.mainMenu.pack(fill = tk.BOTH, expand = True)

    def changeToTutorialMenu(self):
        self.clearWindow()
        self.tutMenu.pack(fill = tk.BOTH, expand = True)

    def changeToNewSimMenu(self):
        self.clearWindow()
        self.newSimMenu.pack(fill = tk.BOTH, expand = True)

class mainFrame(ttk.Frame):
    """mainFrame docstring"""
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.columnconfigure(0, weight = 1, minsize = _MIN_WIN_WIDTH)
        self.rowconfigure([0, 1, 2, 3], weight = 1, minsize = _MIN_WIN_HEIGHT/4)

        self.lbl_nameText = ttk.Label(master = self, text="Cellvolution")
        self.btn_newSim = ttk.Button(master = self, text="New Simulation", command = partial(master.changeToNewSimMenu))
        self.btn_loadSim = ttk.Button(master = self, text="Load Simulation")
        self.btn_loadSim.bind("<Button-1>", master.getFilePath)
        self.btn_tutorial = ttk.Button(master = self, text="Tutorial", command = partial(master.changeToTutorialMenu))

        self.lbl_nameText.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "ns")
        self.btn_newSim.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "nsew")
        self.btn_loadSim.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "nsew")
        self.btn_tutorial.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "nsew")
        
class tutorialFrame(ttk.Frame):
    """tutorialFrame docstring"""
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.columnconfigure(0, weight = 1, minsize = _MIN_WIN_WIDTH)
        self.rowconfigure(0, weight = 1, minsize = _MIN_WIN_HEIGHT-50)
        
        self.btn_return = ttk.Button(master = self, text="Return to Main Menu", command = partial(self.master.changeToMainMenu))
        
        self.txt_tutorial = scrolledtext.ScrolledText(master = self, wrap = tk.WORD)
        self.tutorialFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "tutorial.txt"))
        if(os.path.exists(self.tutorialFilePath)):
            f = open(self.tutorialFilePath, "r")
            self.txt_tutorial.insert(tk.INSERT, f.read())
            f.close()
        
        self.txt_tutorial.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew")
        self.btn_return.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "nsew")

class newSimFrame(ttk.Frame):
    def __init__(self,master):
        ttk.Frame.__init__(self, master)

        #Varibles which hold the various settings the user is modifying,
        #Use of tk control variables allows multiple input methods
        #to control a single value easily and synchronously
        self.envWidth = tk.IntVar(value = 500)
        self.envHeight = tk.IntVar(value = 500)

        self.widthSlider = ttk.Scale(
            orient = tk.HORIZONTAL,
            from_=_MIN_ENV_WIDTH,
            to=_MAX_ENV_WIDTH,
            variable = self.envWidth,
            command = lambda s:self.envWidth.set('%d' % float(s)),
            master = self)
        
        self.widthEntry = ttk.Entry(
            exportselection = 0,
            validate = 'all',
            validatecommand = (self.register(self.validWidth), '%P'),
            textvariable = self.envWidth,
            master = self)
        
        self.widthLabel = ttk.Label(text = 'Environment Width', master = self)

        self.heightSlider = ttk.Scale(
            orient = tk.HORIZONTAL,
            from_=_MIN_ENV_HEIGHT,
            to=_MAX_ENV_HEIGHT,
            variable = self.envHeight,
            command = lambda s:self.envHeight.set('%d' % float(s)),
            master = self)

        self.heightEntry = ttk.Entry(
            exportselection = 0,
            validate = 'all',
            validatecommand = (self.register(self.validHeight), '%P'),
            textvariable = self.envHeight,
            master = self)

        self.heightLabel = ttk.Label(text = 'Environment Height', master = self)

        self.btn_return = ttk.Button(master = self, text="Return to Main Menu", command = partial(self.master.changeToMainMenu))
        self.btn_begin = ttk.Button(master = self, text="Begin Simulation")

        self.columnconfigure([0, 1, 2, 3], weight = 1, minsize = _MIN_WIN_WIDTH/4)
        self.rowconfigure([0, 1, 2, 3, 4, 5], weight = 1, minsize = _MIN_WIN_HEIGHT/6)
        self.widthLabel.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "s")
        self.widthEntry.grid(row = 0, column = 1, padx = 10, pady = 10, sticky = "s")
        self.widthSlider.grid(row = 1, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "new")
        self.heightEntry.grid(row = 2, column = 1, padx = 10, pady = 10, sticky = "s")
        self.heightSlider.grid(row = 3, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "new")
        self.btn_return.grid(row = 5, column = 0, padx = 10, pady = 10, columnspan = 4, sticky = "nsew")
        self.btn_begin.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan = 4, sticky = "nsew")

    def validWidth(self, P):
        if str.isdigit(P) and int(P) >= _MIN_ENV_WIDTH and int(P) <= _MAX_ENV_WIDTH:
            self.envWidth.set(int(P))
            return True 
        if P == "":
            return True
        else:
            return False

    def validHeight(self, P):
        if str.isdigit(P) and int(P) >= _MIN_ENV_HEIGHT and int(P) <= _MAX_ENV_HEIGHT:
            self.envHeight.set(int(P))
            return True 
        if P == "":
            return True
        else:
            return False

