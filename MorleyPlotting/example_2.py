# https://www.geeksforgeeks.org/event-handling-in-matplotlib/

# importing the necessary modules
from IPython.display import Image
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import time
import sys
import random
import matplotlib
matplotlib.use('nbagg')
  
  
class MouseEvent:
    
    # initialization
    def __init__(self):
        (figure, axes) = plt.subplots()
        axes.set_aspect(1)
        figure.canvas.mpl_connect('button_press_event', self.press)
        figure.canvas.mpl_connect('button_release_event', self.release)
  
    # start event to show the plot
    def start(self):
        plt.show()  # display the plot
  
    # press event will keep the starting time when u 
    # press mouse button
    def press(self, event):
        self.start_time = time.time()
  
    # release event will keep the track when you release
    # mouse button
    def release(self, event):
        self.end_time = time.time()
        self.draw_click(event)
  
    # drawing the plot
    def draw_click(self, event):
        # size = square (4 * duration of the time button 
        # is keep pressed )
        size = 4 * (self.end_time - self.start_time) ** 2
          
        # create a point of size=0.002 where mouse button 
        # clicked on the plot
        c1 = plt.Circle([event.xdata, event.ydata], 0.002,)
          
        # create a circle of radius 0.02*size
        c2 = plt.Circle([event.xdata, event.ydata], 0.02 * size, alpha=0.2)
        event.canvas.figure.gca().add_artist(c1)
        event.canvas.figure.gca().add_artist(c2)
        event.canvas.figure.show()
  
  
cbs = MouseEvent()
  
# start the event
cbs.start()