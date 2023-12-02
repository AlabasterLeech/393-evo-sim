"""This module represents the core of Cellvolution, responsible for constructing the GUI and running the eventloop.

"""
#Import statements
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from functools import partial
import os

#Import statements handling other parts of the project
import gui

def main():
    #GUI Main Window Construction
    cellvolutionWindow = gui.gameWindow()
    cellvolutionWindow.changeToMainMenu()
    cellvolutionWindow.mainloop()

    #TODO Instantiate a simulation and attach it and the GUI together

if __name__ == '__main__':
    main()
