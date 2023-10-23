"""This module represents the core of Cellvolution, responsible for constructing the GUI and running the eventloop.

"""
#Import statements
import tkinter as tk
from tkinter import scrolledtext

#Module level constant definitions.
_WINDOW_TITLE = "Cellvolution 1.0"
_MIN_WIDTH = 640
_MIN_HEIGHT = 480

"""Initializes all the widgets for the main menu and returns them inside a frame.

This frame, along with frames for other GUI states, are then packed and unpacked to transition between
GUI states, except where access to individual widgets is needed (e.g. in the simulation window).

Param: a Tk object which will be the master for the returned frame
Return: a tk.Frame containing all the main menu widgets
"""
def initMainMenu(gameWindow):
    frm_mainMenu = tk.Frame(master = gameWindow)
    frm_mainMenu.columnconfigure(0, weight = 1, minsize = _MIN_WIDTH)
    frm_mainMenu.rowconfigure([0, 1, 2, 3], weight = 1, minsize = _MIN_HEIGHT/4)

    lbl_nameText = tk.Label(master = frm_mainMenu, text="Cellvolution")
    btn_newSim = tk.Button(master = frm_mainMenu, text="New Simulation")
    btn_loadSim = tk.Button(master = frm_mainMenu, text="Load Simulation")
    btn_tutorial = tk.Button(master = frm_mainMenu, text="Tutorial")

    lbl_nameText.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew")
    btn_newSim.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "nsew")
    btn_loadSim.grid(row = 2, column = 0, padx = 10, pady = 10, sticky = "nsew")
    btn_tutorial.grid(row = 3, column = 0, padx = 10, pady = 10, sticky = "nsew")

    return frm_mainMenu

"""Initializes all the widgets for the tutorial menu and returns them inside a frame.

This frame, along with frames for other GUI states, are then packed and unpacked to transition between
GUI states, except where access to individual widgets is needed (e.g. in the simulation window).

Param: a Tk object which will be the master for the returned frame
Return: a tk.Frame containing all the tutorial menu widgets
"""
def initTutorialMenu(gameWindow):
    frm_tutMenu = tk.Frame(master = gameWindow)
    frm_tutMenu.columnconfigure(0, weight = 1, minsize = _MIN_WIDTH)
    frm_tutMenu.rowconfigure(0, weight = 1, minsize = _MIN_HEIGHT-50)
    
    btn_return = tk.Button(master = frm_tutMenu, text="Return to Main Menu")
    
    txt_tutorial = scrolledtext.ScrolledText(master = frm_tutMenu, wrap = tk.WORD)
    txt_tutorial.insert(tk.INSERT, "")
    txt_tutorial.grid(row = 0, column = 0, padx = 10, pady = 10, sticky = "nsew")
    btn_return.grid(row = 1, column = 0, padx = 10, pady = 10, sticky = "nsew")
    return frm_tutMenu
    

"""Method to forget everything currently being displayed in the game window.
IMPORTANT: This does not deallocate the memory for the frames/widgets which means they can be reused
but also means they should not be recreated as this could lead to memory leakage.

Param: a Tk object representing the window to be cleared.
"""
def clearWindow(gameWindow):
    for widget in gameWindow.winfo_children():
        widget.grid_forget()

def main():
    #GUI Main Window Construction
    gameWindow = tk.Tk()
    gameWindow.title(_WINDOW_TITLE)
    gameWindow.minsize(_MIN_WIDTH,_MIN_HEIGHT)
    gameWindow.rowconfigure(0, weight = 1)
    gameWindow.columnconfigure(0, weight = 1)
    
    #Initialize all the menu frames needed, then load the main menu and start the window loop.
    frm_mainMenu = initMainMenu(gameWindow)
    frm_tutMenu = initTutorialMenu(gameWindow)
    frm_mainMenu.grid(row = 0, column = 0, sticky="nsew")
    gameWindow.mainloop()


if __name__ == '__main__':
    main()
