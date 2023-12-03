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
import GUI

def main():
    #GUI Main Window Construction
    cellvolutionWindow = GUI.gameWindow()
    cellvolutionWindow.changeToMainMenu()
    
    #GUI Event loop and simulation game loop
    #This replaces the 'mainloop()' call in
    #regular TK GUI programs
    
    #TODO: add logic that calls the simulation's
    #step() and step_gen() functions at reasonable/correct
    #frequency inside this loop
    while(True):
        cellvolutionWindow.simCanvasUpdate()
        cellvolutionWindow.update()

if __name__ == '__main__':
    main()
