"""This module represents the core of Cellvolution, responsible for constructing the GUI and running the eventloop.

"""
#Import statements
import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
from tkinter import filedialog
from functools import partial
import os
import time

#Import statements handling other parts of the project
import gui

#Module Level Constant definitions
_SIM_STEP_TIME = 10000000000 #Time between step() calls in the simulation, in nanoseconds. (100,000,000ns = 1/10th of a second)
_CANVAS_UPDATE_FREQ = 10 #How many step() calls between each canvas update. Canvas will also update on the first step of any generation

def main():
    #GUI Main Window Construction
    cellvolutionWindow = gui.gameWindow()
    cellvolutionWindow.changeToMainMenu()
    
    #GUI Event loop and simulation game loop
    #This replaces the 'mainloop()' call in
    #regular TK GUI programs
    while(True):
        curTime = time.perf_counter_ns()
        if(curTime - cellvolutionWindow.lastStepTime > _SIM_STEP_TIME and cellvolutionWindow.paused == False):
            cellvolutionWindow.attachedSimulation.step()
            curTime = time.perf_counter_ns()
        if(cellvolutionWindow.attachedSimulation.age % _CANVAS_UPDATE_FREQ == 1 and cellvolutionWindow.paused == False):
            cellvolutionWindow.simCanvasUpdate()
            cellvolutionWindow.simDataUpdate()
        cellvolutionWindow.update()

        #This try/except block checks if the window still exists, if it doesn't it breaks the loop
        #monitoring the events for that window, which will terminate the program
        #Thus if the window is closed by some OS function (like the X button in the corner)
        #the program properly terminates.
        try:
            cellvolutionWindow.state()
        except:
            break

if __name__ == '__main__':
    main()
