"""This module represents the core of Cellvolution, responsible for constructing the GUI and running the eventloop.

"""
#Import statements
import tkinter as tk
from tkinter import scrolledtext
from tkinter import filedialog
from functools import partial
import os

#Module level constant definitions.
_WINDOW_TITLE = "Cellvolution 1.0"
_MIN_WIDTH = 640
_MIN_HEIGHT = 480

"""Method to forget everything currently being displayed in the game window.
IMPORTANT: This does not deallocate the memory for the frames/widgets which means they can be reused
but also means they should not be recreated as this could lead to memory leakage.

Param: a Tk object representing the window to be cleared.
"""
def clearWindow(gameWindow):
    for widget in gameWindow.winfo_children():
        widget.pack_forget()

def main():
    #GUI Main Window Construction
    gameWindow = tk.Tk()
    gameWindow.title(_WINDOW_TITLE)
    gameWindow.minsize(_MIN_WIDTH,_MIN_HEIGHT)
    
    #Initialize the menu frames
    frm_mainMenu = tk.Frame(master = gameWindow)
    frm_tutMenu = tk.Frame(master = gameWindow)

    #Holds the file path for loading or saving the simulation
    simFilePath = None
    
    #Function buttons call to change out frames
    def changeToFrame(frame):
        clearWindow(gameWindow)
        frame.pack(fill = tk.BOTH, expand = True)

    #Function to prompt the user to select a file to load and then store its path in simFilePath
    def getFilePath(*options):
        simFilePath = filedialog.askopenfilename(parent = gameWindow, filetypes=[("JSON Files", "*.json")])

    #Populate the main menu
    frm_mainMenu.columnconfigure(0, weight = 1, minsize = _MIN_WIDTH)
    frm_mainMenu.rowconfigure([0, 1, 2, 3], weight = 1, minsize = _MIN_HEIGHT/4)

    lbl_nameText = tk.Label(master = frm_mainMenu, text="Cellvolution")
    btn_newSim = tk.Button(master = frm_mainMenu, text="New Simulation")
    btn_loadSim = tk.Button(master = frm_mainMenu, text="Load Simulation")
    btn_loadSim.bind("<Button-1>", getFilePath)
    btn_tutorial = tk.Button(master = frm_mainMenu, text="Tutorial", command = partial(changeToFrame, frm_tutMenu))

    lbl_nameText.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew")
    btn_newSim.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "nsew")
    btn_loadSim.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "nsew")
    btn_tutorial.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "nsew")

    #Populate the tutorial menu
    frm_tutMenu.columnconfigure(0, weight = 1, minsize = _MIN_WIDTH)
    frm_tutMenu.rowconfigure(0, weight = 1, minsize = _MIN_HEIGHT-50)
    
    btn_return = tk.Button(master = frm_tutMenu, text="Return to Main Menu", command = partial(changeToFrame, frm_mainMenu))
    
    txt_tutorial = scrolledtext.ScrolledText(master = frm_tutMenu, wrap = tk.WORD)
    tutorialFilePath = os.path.normpath(os.path.join(os.path.abspath(__file__), "..", "..", "assets", "tutorial.txt"))
    if(os.path.exists(tutorialFilePath)):
        f = open(tutorialFilePath, "r")
        txt_tutorial.insert(tk.INSERT, f.read())
        f.close()
    
    txt_tutorial.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew")
    btn_return.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "nsew")


    #Load the main menu and run the window loop
    changeToFrame(frm_mainMenu)
    gameWindow.mainloop()


if __name__ == '__main__':
    main()
