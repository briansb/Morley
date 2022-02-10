# see Version_1.py

import pdb
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class MoveableCircle(object):
    def __init__(self, circle):
        self.circle = circle
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.circle.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.circle.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.circle.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        #  The Axes instance contains most of the elements on the plot
        if event.inaxes != self.circle.axes: return  # not inside the plot (or axes)
        contains, attrd = self.circle.contains(event) # not inside the circle
        if not contains: return
        print(f"{self.circle.get_label()} was pressed with x0, y0 = {self.circle.center}, mouse x,y = {event.xdata}, {event.ydata}")
        x0, y0 = self.circle.center  # lower left coordinates of circle
        # will check for the presence of this data in the on_motion event
        self.press = x0, y0, event.xdata, event.ydata  # .xdata, .ydata are coordinates of mouse when pressed

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.circle.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will move the circle if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.circle.axes: return
        x0, y0, xpress, ypress = self.press  # retrieve the data from the mouse press event
        dx = event.xdata - xpress  # this is how far the mouse has moved
        dy = event.ydata - ypress
        xy = (x0 + dx, y0 + dy)  # set the circle origin to the new position

        x, y = self.circle.center
        x = x0 + dx
        y = y0 + dy
        self.circle.center = (x, y)

        self.circle.figure.canvas.draw()


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.circle.figure.canvas.mpl_disconnect(self.cidpress)
        self.circle.figure.canvas.mpl_disconnect(self.cidrelease)
        self.circle.figure.canvas.mpl_disconnect(self.cidmotion)

###############################################################################################

class MoveableSquare(object):
    def __init__(self, square, lines):
        self.square = square
        self.lines = lines
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.square.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.square.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.square.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        #  The Axes instance contains most of the elements on the plot
        if event.inaxes != self.square.axes: return  # not inside the plot (or axes)
        contains, attrd = self.square.contains(event) # not inside the square
        if not contains: return
        print(f"{self.square.get_label()} was pressed with x0, y0 = {self.square.xy}, mouse x,y = {event.xdata}, {event.ydata}")
        x0, y0 = self.square.xy  # lower left coordinates of square
        # will check for the presence of this data in the on_motion event
        self.press = x0, y0, event.xdata, event.ydata  # .xdata, .ydata are coordinates of mouse when pressed

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.square.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will move the square if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.square.axes: return
        x0, y0, xpress, ypress = self.press  # retrieve the data from the mouse press event
        dx = event.xdata - xpress  # this is how far the mouse has moved
        dy = event.ydata - ypress
        self.square.set_x(x0+dx)  # set the square origin to the new position
        self.square.set_y(y0+dy)

        for ii in range(2):        #  set the beginning line points to the new position
           x = self.lines[ii].get_xdata()
           y = self.lines[ii].get_ydata()
           x[0] = x0 + dx
           y[0] = y0 + dy
           self.lines[ii].set_xdata(x)
           self.lines[ii].set_ydata(y)

        self.square.figure.canvas.draw()


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.square.figure.canvas.mpl_disconnect(self.cidpress)
        self.square.figure.canvas.mpl_disconnect(self.cidrelease)
        self.square.figure.canvas.mpl_disconnect(self.cidmotion)

#####################################################################

fig = plt.figure(figsize=(12,6))
axes = plt.axes()
axes.set_xlim([-1,12])
axes.set_ylim([-1,6])

x_start = 2
y_start = 2
square1 = plt.Rectangle((x_start, y_start), 1, 1, fc='yellow',ec="yellow", label="unus")
plt.gca().add_patch(square1)

square2 = plt.Rectangle((x_start + 6, y_start + 1), 1, 1, fc='red',ec="red", label="duo")
plt.gca().add_patch(square2)

x = [x_start, 10]
y = [y_start, 5]
line1 = plt.Line2D(x, y, color='green', linewidth = 4)
plt.gca().add_line(line1)
lines = []
lines.append(line1)

x = [x_start, 9]
y = [y_start, 0]
line2 = plt.Line2D(x, y, color='green', linewidth = 4)
plt.gca().add_line(line2)
lines.append(line2)

text1 = plt.text(0,1, 'y = ax + b', fontsize=16, rotation=30, rotation_mode='anchor')

squares = []
square = MoveableSquare(square1, lines)
square.connect()
squares.append(square)
square = MoveableSquare(square2, lines)
square.connect()
squares.append(square)

#drs = []
# rects = plt.bar(range(3), 10*np.random.rand(3))
# for rect in rects:
#     dr = DraggableRectangle(rect)
#     dr.connect()
#     drs.append(dr)




circle1 = plt.Circle((2, 4), 0.5, fc="blue", ec="blue", label="tres")
plt.gca().add_patch(circle1)
circle = MoveableCircle(circle1)
circle.connect()

plt.show()