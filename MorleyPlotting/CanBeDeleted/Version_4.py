# https://stackoverflow.com/questions/43982250/draggable-markers-in-matplotlib

import numpy as np
import matplotlib.pyplot as plt

x = np.arange(60)
y = np.sin(x)*np.log(x+1)

fig, ax = plt.subplots()
ax.plot(x,y, marker="o", ms=4)

class DraggableMarker():
    def __init__(self,ax=None, lines=None):
        if ax == None:
            self.ax = plt.gca()
        else:
            self.ax=ax
        if lines==None:
            self.lines=self.ax.lines
        else:
            self.lines=lines
        self.lines = self.lines[:]
        self.tx =  [self.ax.text(0,0,"") for l in self.lines]
        self.marker = [self.ax.plot([0],[0], marker="o", color="red")[0]  for l in self.lines]

        self.draggable=False
        
        self.c1 = self.ax.figure.canvas.mpl_connect("button_press_event", self.click)
        self.c2 = self.ax.figure.canvas.mpl_connect("button_release_event", self.release)
        self.c3 = self.ax.figure.canvas.mpl_connect("motion_notify_event", self.drag)
    
    def click(self,event):
        if event.button==1:
            #leftclick
            self.draggable=True
            self.update(event)
        elif event.button==3:
            self.draggable=False
        [tx.set_visible(self.draggable) for tx in self.tx]
        [m.set_visible(self.draggable) for m in self.marker]
        ax.figure.canvas.draw_idle()        
                
    def drag(self, event):
        if self.draggable:
            self.update(event)
            ax.figure.canvas.draw_idle()

    def release(self,event):
        self.draggable=False
        
    def update(self, event):
        for i, line in enumerate(self.lines):
            x,y = self.get_closest(line, event.xdata) 
            self.tx[i].set_position((x,y))
            self.tx[i].set_text("x:{}\ny:{}".format(x,y))
            self.marker[i].set_data([x],[y])
            
    def get_closest(self,line, mx):
        x,y = line.get_data()
        mini = np.argmin(np.abs(x-mx))
        return x[mini], y[mini]
    
dm = DraggableMarker()

plt.show()