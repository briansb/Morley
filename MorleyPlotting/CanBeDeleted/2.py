# https://matplotlib.org/3.1.0/users/event_handling.html

import pdb
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
pi = math.acos(-1.0)
radian_to_degrees = 360.0 / (2.0 * pi)

class MoveableCircle(object):
    def __init__(self, circle, lines, vertices):
        self.circle = circle
        self.lines = lines
        self.vertices = vertices
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.circle.figure.canvas.mpl_connect('button_press_event', self.on_press)
        self.cidrelease = self.circle.figure.canvas.mpl_connect('button_release_event', self.on_release)
        self.cidmotion = self.circle.figure.canvas.mpl_connect('motion_notify_event', self.on_motion)

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.circle.figure.canvas.draw()

    def disconnect(self):
        'disconnect all the stored connection ids'
        self.circle.figure.canvas.mpl_disconnect(self.cidpress)
        self.circle.figure.canvas.mpl_disconnect(self.cidrelease)
        self.circle.figure.canvas.mpl_disconnect(self.cidmotion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        #  The Axes instance contains most of the elements on the plot
        if event.inaxes != self.circle.axes: return  # not inside the plot (or axes)
        contains, attrd = self.circle.contains(event) # not inside the circle
        if not contains: return   # it iterates through all circles, somehow
        #print(f"{self.circle.get_label()} was pressed with x0, y0 = {self.circle.center}, mouse x,y = {event.xdata}, {event.ydata}")
        x0, y0 = self.circle.center  # center coordinates of circle
        # will check for the presence of this data in the on_motion event
        self.press = x0, y0, event.xdata, event.ydata  # .xdata, .ydata are coordinates of mouse when pressed

    def on_motion(self, event):
        'on motion we will move the circle if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.circle.axes: return
        x0, y0, xpress, ypress = self.press  # retrieve the data from the mouse press event
        dx = event.xdata - xpress  # this is how far the mouse has moved
        dy = event.ydata - ypress
        xy = (x0 + dx, y0 + dy)  # set the circle origin to the new position

        # move circle to new position
        x, y = self.circle.center
        x = x0 + dx
        y = y0 + dy
        self.circle.center = (x, y)

        # re-draw lines, move vertex text (coordinates), compute and display slope and y-intercept
        if self.circle.get_label() == "unus":
            self.redraw_lines(event, x0, y0, dx, dy, 0, 2)
            self.redraw_vertex_text(event, 0)

        elif self.circle.get_label() == "duo":
            self.redraw_lines(event, x0, y0, dx, dy, 1, 0)
            self.redraw_vertex_text(event, 1)

        elif self.circle.get_label() == "tres":
            self.redraw_lines(event, x0, y0, dx, dy, 2, 1)
            self.redraw_vertex_text(event, 2)

        else:
            print("Should not be here - statement 1")

        # re-draw the whole thing
        self.circle.figure.canvas.draw()
        #  end of on_motion event

    def redraw_lines(self, event, x0, y0, dx, dy, i, j):
        x = self.lines[i].get_xdata()
        y = self.lines[i].get_ydata()
        x[0] = x0 + dx
        y[0] = y0 + dy
        self.lines[i].set_xdata(x)
        self.lines[i].set_ydata(y)

        x = self.lines[j].get_xdata()
        y = self.lines[j].get_ydata()
        x[1] = x0 + dx
        y[1] = y0 + dy
        self.lines[j].set_xdata(x)
        self.lines[j].set_ydata(y)
        
    def redraw_vertex_text(self, event, i):
        newx, newy = self.circle.center
        text = f'({newx:.1f},{newy:.1f})'
        if i == 0:
            self.vertices[i].set_x(newx - 0.15*len(text))
            self.vertices[i].set_y(newy - 0.01*len(text))
        if i == 1:
            self.vertices[i].set_x(newx + 0.04*len(text))
            self.vertices[i].set_y(newy - 0.01*len(text))
        if i == 2:
            self.vertices[i].set_x(newx - 0.05*len(text))
            self.vertices[i].set_y(newy -  0.06*len(text))
        self.vertices[i].set_text(text)



##################################   Main    ######################################
fig = plt.figure(figsize=(12,6))
axes = plt.axes()
axes.set_xlim([-1,12])
axes.set_ylim([-1,6])

# initial values
ux = 2
uy = 5
vx = 10
vy = 3
wx = 4
wy = 0
radius = 0.25
lines = []
vertices = []
circles = []

########################## lines 1,2,3 ###########################################

x = [ux, vx]
y = [uy, vy]
line1 = plt.Line2D(x, y, color='black', linewidth = 4)
plt.gca().add_line(line1)
lines.append(line1)

x = [vx, wx]
y = [vy, wy]
line2 = plt.Line2D(x, y, color='black', linewidth = 4)
plt.gca().add_line(line2)
lines.append(line2)

x = [wx, ux]
y = [wy, uy]
line3 = plt.Line2D(x, y, color='black', linewidth = 4)
plt.gca().add_line(line3)
lines.append(line3)

########################### vertices 1,2,3 #############################################

text = f'({ux:.1f},{uy:.1f})'
vertex1 = plt.text(ux - 0.15*len(text), uy - 0.01*len(text), text, fontsize=12, rotation=0, rotation_mode='anchor')
vertices.append(vertex1)

text = f'({vx:.1f},{vy:.1f})'
vertex2 = plt.text(vx + 0.04*len(text), vy - 0.01*len(text), text, fontsize=12, rotation=0, rotation_mode='anchor')
vertices.append(vertex2)

text = f'({wx:.1f},{wy:.1f})'
vertex3 = plt.text(wx - 0.05*len(text), wy - 0.06*len(text), text, fontsize=12, rotation=0, rotation_mode='anchor')
vertices.append(vertex3)

###########################  circles 1,2,3 ######################################################

circle1 = plt.Circle((ux, uy), radius, fc="blue", label="unus")
plt.gca().add_patch(circle1)
circle = MoveableCircle(circle1, lines, vertices)
circle.connect()
circles.append(circle)

circle2 = plt.Circle((vx, vy), radius, fc="blue", label="duo")
plt.gca().add_patch(circle2)
circle = MoveableCircle(circle2, lines, vertices)
circle.connect()
circles.append(circle)

circle3 = plt.Circle((wx, wy), radius, fc="blue", label="tres")
plt.gca().add_patch(circle3)
circle = MoveableCircle(circle3, lines, vertices)
circle.connect()
circles.append(circle)

plt.show()