"""This module contains the classes which define the GUI.

"""
#Import statements
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from functools import partial
from PIL import Image, ImageTk
import os

#Module level constant definitions.
_WINDOW_TITLE = "Cellvolution 1.0"
_MIN_WIN_WIDTH = 640
_MIN_WIN_HEIGHT = 480
_MAX_ENV_WIDTH = 1000
_MIN_ENV_WIDTH = 10
_MAX_ENV_HEIGHT = 1000
_MIN_ENV_HEIGHT = 10
_MIN_FOOD_DENSITY = 5
_MAX_FOOD_DENSITY = 25
_MIN_NUM_ORGANISMS = 100
_MAX_NUM_ORGANISMS = 10000
_SIM_BUTTON_DEFAULT_SIZE = 50



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
        #self.maxsize(_MIN_WIN_WIDTH,_MIN_WIN_HEIGHT)
        self.minsize(_MIN_WIN_WIDTH,_MIN_WIN_HEIGHT)
        self.mainMenu = mainFrame(self)
        self.tutMenu = tutorialFrame(self)
        self.newSimMenu = newSimFrame(self)
        self.simulationMenu = simulationFrame(self)
        self.attachedSimulation = None
        self.simFilePath = None
        #self.resizable(False, False)
        try:
            iconFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "cellvolution_icon.ico"))
            self.iconbitmap(iconFilePath)
        except:
            print("Failure loading icon")
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

    def changeToSimulationMenu(self):
        self.clearWindow()
        self.simulationMenu.pack(fill = tk.BOTH, expand = True)

    def attachSimulation(self, simulation):
        self.attachedSimulation = simulation

class mainFrame(ttk.Frame):
    """mainFrame docstring"""
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure([0, 1, 2, 3], weight = 1)

        self.lbl_name = ttk.Label(master = self)
        self.btn_newSim = ttk.Button(master = self, text="New Simulation", command = partial(master.changeToNewSimMenu))
        self.btn_loadSim = ttk.Button(master = self, text="Load Simulation")
        self.btn_loadSim.bind("<Button-1>", master.getFilePath)
        self.btn_tutorial = ttk.Button(master = self, text="Tutorial", command = partial(master.changeToTutorialMenu))

        try:
            logoFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "logo.png"))
            self.logoImg = ImageTk.PhotoImage(Image.open(logoFilePath))
            self.lbl_name.config(image = self.logoImg)
        except:
            self.lbl_name.config(text = "Cellvolution")
        
        self.lbl_name.grid(row = 0, column = 0, sticky = "ns", pady = 10, padx = 10)
        self.btn_newSim.grid(row = 1, column = 0, sticky = "nsew", pady = 10, padx = 10)
        self.btn_loadSim.grid(row = 2, column = 0, sticky = "nsew", pady = 10, padx = 10)
        self.btn_tutorial.grid(row = 3, column = 0, sticky = "nsew", pady = 10, padx = 10)

        
            
        
class tutorialFrame(ttk.Frame):
    """tutorialFrame docstring"""
    def __init__(self, master):
        ttk.Frame.__init__(self, master)

        self.columnconfigure(0, weight = 1)
        self.rowconfigure(0, weight = 1)
        
        self.btn_return = ttk.Button(master = self, text="Return to Main Menu", command = partial(self.master.changeToMainMenu))
        
        self.txt_tutorial = scrolledtext.ScrolledText(master = self, wrap = tk.WORD)
        self.tutorialFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "tutorial.txt"))
        if(os.path.exists(self.tutorialFilePath)):
            f = open(self.tutorialFilePath, "r")
            self.txt_tutorial.insert(tk.INSERT, f.read())
            f.close()
        
        self.txt_tutorial.grid(row = 0, column = 0, sticky = "nsew", padx = 10)
        self.btn_return.grid(row = 1, column = 0, sticky = "nsew", pady = 10, padx = 10)

class newSimFrame(ttk.Frame):
    """newSimFrame docstring"""
    def __init__(self,master):
        ttk.Frame.__init__(self, master)

        #Varibles which hold the various settings the user is modifying,
        #Use of tk control variables allows multiple input methods
        #to control a single value easily and synchronously
        self.envWidth = tk.IntVar(value = 500)
        self.envHeight = tk.IntVar(value = 500)
        self.foodDensity = tk.IntVar(value = 10)
        self.numOrganisms = tk.IntVar(value = 1000)
        self.survivalFunction = tk.StringVar(value = "None")

        #Make all them widgets
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
            validatecommand = (self.register(self.validateWidth), '%P'),
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
            validatecommand = (self.register(self.validateHeight), '%P'),
            textvariable = self.envHeight,
            master = self)

        self.heightLabel = ttk.Label(text = 'Environment Height', master = self)

        self.foodDensitySlider = ttk.Scale(
            orient = tk.HORIZONTAL,
            from_=_MIN_FOOD_DENSITY,
            to=_MAX_FOOD_DENSITY,
            variable = self.foodDensity,
            command = lambda s:self.foodDensity.set('%d' % float(s)),
            master = self)
        
        self.foodDensityEntry = ttk.Entry(
            exportselection = 0,
            validate = 'all',
            validatecommand = (self.register(self.validateFoodDensity), '%P'),
            textvariable = self.foodDensity,
            master = self)
        
        self.foodDensityLabel = ttk.Label(text = 'Food Density (%)', master = self)

        self.numOrganismsSlider = ttk.Scale(
            orient = tk.HORIZONTAL,
            from_=_MIN_NUM_ORGANISMS,
            to=_MAX_NUM_ORGANISMS,
            variable = self.numOrganisms,
            command = lambda s:self.numOrganisms.set('%d' % float(s)),
            master = self)
        
        self.numOrganismsEntry = ttk.Entry(
            exportselection = 0,
            validate = 'all',
            validatecommand = (self.register(self.validateNumOrganisms), '%P'),
            textvariable = self.numOrganisms,
            master = self)
        
        self.numOrganismsLabel = ttk.Label(text = 'Initial Number Of Organisms', master = self)

        self.survivalFunctionSelector = ttk.Combobox(
            exportselection = 0,
            state = "readonly",
            textvariable = self.survivalFunction,
            height = 5,
            values = ["None", "Has Eaten Food", "Temp Surv Func 1", "Temp Surv Func 3"],
            master = self)

        self.survivalFunctionLabel = ttk.Label(text = 'Survival Function', master = self)

        self.btn_return = ttk.Button(master = self, text="Return to Main Menu", command = partial(self.master.changeToMainMenu))
        self.btn_begin = ttk.Button(master = self, text="Begin Simulation", command = partial(self.master.changeToSimulationMenu)) #TODO: pass values to attached simulation

        #Set up the geometry of all the widgets
        self.columnconfigure([0, 1, 2, 3], weight = 1, minsize = _MIN_WIN_WIDTH/4)
        self.rowconfigure([0, 1, 2, 3, 4, 5, 6], weight = 1, minsize = _MIN_WIN_HEIGHT/7)

        self.survivalFunctionLabel.grid(row = 0, column = 0, padx = 10, pady = 10)
        self.survivalFunctionSelector.grid(row = 0, column = 1, padx = 10, pady = 10, columnspan = 3, sticky = "ew")

        self.widthLabel.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "s")
        self.widthEntry.grid(row = 1, column = 1, padx = 10, pady = 10, sticky = "s")
        self.widthSlider.grid(row = 2, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "new")

        self.heightEntry.grid(row = 3, column = 1, padx = 10, pady = 10, sticky = "s")
        self.heightLabel.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "s")
        self.heightSlider.grid(row = 4, column = 0, padx = 10, pady = 10, columnspan = 2, sticky = "new")

        self.foodDensityLabel.grid(row = 1, column = 2, padx = 10, pady = 10, sticky = "s")
        self.foodDensityEntry.grid(row = 1, column = 3, padx = 10, pady = 10, sticky = "s")
        self.foodDensitySlider.grid(row = 2, column = 2, padx = 10, pady = 10, columnspan = 2, sticky = "new")

        self.numOrganismsLabel.grid(row = 3, column = 2, padx = 10, pady = 10, sticky = "s")
        self.numOrganismsEntry.grid(row = 3, column = 3, padx = 10, pady = 10, sticky = "s")
        self.numOrganismsSlider.grid(row = 4, column = 2, padx = 10, pady = 10, columnspan = 2, sticky = "new")

        self.btn_return.grid(row = 6, column = 0, padx = 10, pady = 10, columnspan = 4, sticky = "nsew")
        self.btn_begin.grid(row = 5, column = 0, padx = 10, pady = 10, columnspan = 4, sticky = "nsew")

    def validateWidth(self, P):
        """Validates that the value of the width widget is an integer and inside the bounds set by the constants.
        Called by the widget's internal validation functionality."""
        if str.isdigit(P) and int(P) >= _MIN_ENV_WIDTH and int(P) <= _MAX_ENV_WIDTH:
            self.envWidth.set(int(P))
            return True 
        if P == "":
            return True
        else:
            return False

    def validateHeight(self, P):
        """Validates that the value of the height widget is an integer and inside the bounds set by the constants.
        Called by the widget's internal validation functionality."""
        if str.isdigit(P) and int(P) >= _MIN_ENV_HEIGHT and int(P) <= _MAX_ENV_HEIGHT:
            self.envHeight.set(int(P))
            return True 
        if P == "":
            return True
        else:
            return False

    def validateFoodDensity(self, P):
        """Validates that the value of the food density widget is an integer and inside the bounds set by the constants.
        Called by the widget's internal validation functionality."""
        if str.isdigit(P) and int(P) >= _MIN_FOOD_DENSITY and int(P) <= _MAX_FOOD_DENSITY:
            self.foodDensity.set(int(P))
            return True 
        if P == "":
            return True
        else:
            return False

    def validateNumOrganisms(self, P):
        """Validates that the value of the num organisms widget is an integer and inside the bounds set by the constants.
        Called by the widget's internal validation functionality."""
        if str.isdigit(P) and int(P) >= _MIN_NUM_ORGANISMS and int(P) <= _MAX_NUM_ORGANISMS:
            self.numOrganisms.set(int(P))
            return True 
        if P == "":
            return True
        else:
            return False
        
class simulationFrame(ttk.Frame):
    """simulationFrame docstring"""
    def __init__(self,master):
        ttk.Frame.__init__(self, master)

        self.canvasFrame = ttk.Frame(master = self)
        self.canvasHorizScrollBar = tk.Scrollbar(master = self.canvasFrame, orient = 'horizontal')
        self.canvasVertiScrollBar = tk.Scrollbar(master = self.canvasFrame, orient = 'vertical')
        #in the near future this canvas will be initilized with values grabbed from the simulation, but for now it has dummy values.
        self.simDisplayCanvas = tk.Canvas(master = self.canvasFrame, scrollregion = (0,0,1000,1000),
                                          xscrollcommand = self.canvasHorizScrollBar.set, yscrollcommand = self.canvasVertiScrollBar.set)
        self.canvasHorizScrollBar.config(command = self.simDisplayCanvas.xview)
        self.canvasVertiScrollBar.config(command = self.simDisplayCanvas.yview)

        #placeholder canvas background until the simulation class is complete
        try:
            bgFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "testimage.png"))
            self.bgImg = ImageTk.PhotoImage(Image.open(bgFilePath))
            self.simDisplayCanvas.create_image(500, 500, image = self.bgImg)
        except:
            self.simDisplayCanvas.config(bg = "red")
            
        self.canvasHorizScrollBar.pack(side = 'bottom', fill = 'x')
        self.canvasVertiScrollBar.pack(side = 'left', fill = 'y')
        self.simDisplayCanvas.pack(side= 'bottom', fill = 'both', expand = 1)

        self.btn_play = ttk.Button(master = self)
        try:
            playIconFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "play.png"))
            self.playIcon = ImageTk.PhotoImage(Image.open(playIconFilePath))
            self.btn_play.config(image = self.playIcon)
        except:
            self.btn_play.config(text = "Play")

        self.btn_pause = ttk.Button(master = self)
        try:
            pauseIconFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "pause.png"))
            self.pauseIcon = ImageTk.PhotoImage(Image.open(pauseIconFilePath))
            self.btn_pause.config(image = self.pauseIcon)
        except:
            self.btn_pause.config(text = "Pause")

        self.btn_advance_one = ttk.Button(master = self)
        try:
            advance_oneIconFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "advance_one.png"))
            self.advance_oneIcon = ImageTk.PhotoImage(Image.open(advance_oneIconFilePath))
            self.btn_advance_one.config(image = self.advance_oneIcon)
        except:
            self.btn_advance_one.config(text = "Advance One Generation")
            
        self.btn_save = ttk.Button(master = self)
        try:
            saveIconFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "save.png"))
            self.saveIcon = ImageTk.PhotoImage(Image.open(saveIconFilePath))
            self.btn_save.config(image = self.saveIcon)
        except:
            self.btn_save.config(text = "Save")

        self.btn_modify = ttk.Button(master = self)
        try:
            modifyIconFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "modify.png"))
            self.modifyIcon = ImageTk.PhotoImage(Image.open(modifyIconFilePath))
            self.btn_modify.config(image = self.modifyIcon)
        except:
            self.btn_modify.config(text = "Modify Simulation")

        self.btn_exit = ttk.Button(master = self, command = partial(self.master.changeToMainMenu))
        try:
            exitIconFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "exit.png"))
            self.exitIcon = ImageTk.PhotoImage(Image.open(exitIconFilePath))
            self.btn_exit.config(image = self.exitIcon)
        except:
            self.btn_exit.config(text = "Exit Simulation")
        
        #set up the geometry of all the widgets
        self.columnconfigure([0, 1, 2, 3, 4 ,5], weight = 1, minsize = _SIM_BUTTON_DEFAULT_SIZE)
        self.columnconfigure(6, weight = 2, minsize = 180)
        self.rowconfigure(0, weight = 7, minsize = _SIM_BUTTON_DEFAULT_SIZE)
        self.rowconfigure(1, weight = 1, minsize = _SIM_BUTTON_DEFAULT_SIZE)

        self.canvasFrame.grid(row = 0, column = 0, columnspan = 6, sticky = "nsew")
        self.btn_play.grid(row = 1, column = 0, sticky = "nsew")
        self.btn_pause.grid(row = 1, column = 1, sticky = "nsew")
        self.btn_advance_one.grid(row = 1, column = 2, sticky = "nsew")
        self.btn_save.grid(row = 1, column = 3, sticky = "nsew")
        self.btn_modify.grid(row = 1, column = 4, sticky = "nsew")
        self.btn_exit.grid(row = 1, column = 5, sticky = "nsew")
