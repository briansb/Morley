# https://matplotlib.org/3.1.0/users/event_handling.html

####  Plan  ####
#  1.  Draw circles
#  2.  Draw vertex text
#  3.  Draw exterior lines
#  4.  Get interior angles


#  Then, on_motion, re-draw everybody


from ast import AsyncFunctionDef
import pdb
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def Vertex_text(x, y):
    return f'({x:.1f},{y:.1f})'

def GetInteriorAngle(i,j):
    # compute vector1 from line i
    # compute vector2 from line j
    # compute stuff

class MoveableCircle(object):
    def __init__(self, circle, vertices, vertex_text, lines):
        self.circle = circle
        self.vertices = vertices
        self.vertex_text = vertex_text
        self.lines = lines
        self.press = None

    def redraw_line(self, i, j, x, y):
        xdata = self.lines[i].get_xdata()
        ydata = self.lines[i].get_ydata()
        xdata[1] = x
        ydata[1] = y
        self.lines[i].set_xdata(xdata)
        self.lines[i].set_ydata(ydata)

        xdata = self.lines[j].get_xdata()
        ydata = self.lines[j].get_ydata()
        xdata[0] = x
        ydata[0] = y
        self.lines[j].set_xdata(xdata)
        self.lines[j].set_ydata(ydata)

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
        x, y = self.circle.center  # center coordinates of circle
        # will check for the presence of this data in the on_motion event
        self.press = x, y, event.xdata, event.ydata  # .xdata, .ydata are coordinates of mouse when pressed

    def on_motion(self, event):
        'on motion we will move the circle if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.circle.axes: return
        x, y, xpress, ypress = self.press  # retrieve the data from the mouse press event
        dx = event.xdata - xpress  # this is how far the mouse has moved
        dy = event.ydata - ypress
        x += dx
        y += dy
        # 1. Re-draw circle
        self.circle.center = (x, y)

        # update u, v, w so that the new values are available to any item
        if self.circle.get_label() == "unus":
            index = 0
        elif self.circle.get_label() == "duo":
            index = 1
        elif self.circle.get_label() == "tres":
            index = 2
        self.vertices[index] = (x,y)

        #  2.  Re-draw vertex text
        text = Vertex_text(x, y)
        self.vertex_text[index].set_text(text)

        #  3.  Re-draw exterior lines
        if index == 0:    # re-draw lines 3 and 1
            # x, y are the new end point of line 3
            # x, y are the new beginning point of line 1
            self.redraw_line(2, 0, x, y)
        elif index == 1:  # re-draw lines 1 and 2
            self.redraw_line(0, 1, x, y)
        elif index == 2:  # re-draw lines 2 and 3
            self.redraw_line(1, 2, x, y)

        #  4.  Get interior angles


        self.circle.figure.canvas.draw()
    ######  end of on_motion event  ##################

    

##################################   Main    ######################################

vertices = []       # u, v, and w
circles = []        # circles are plt.Circle()
vertex_text = []    # vertex_text are plt.text
lines = []          # lines are the exterior (1-3) and interior lines (4-9)
interior_angles_text = []  # interior_angles_text are plt.text

fig = plt.figure(figsize=(16,10))
axes = plt.axes()
axes.set_xlim([-2,14])
axes.set_ylim([-2,8])
# for testing with Plot 2
# axes.set_xlim([-16,36])
# axes.set_ylim([-6,26])
font_size = 12
radius = 0.25

# set the three vertices
u = Point(2, 5)
v = Point(10, 3)
w = Point(4, 0)

vertices.append(u)
vertices.append(v)
vertices.append(w)

###########################  circles 1,2,3 ######################################################
#  1. Draw circles

circle1 = plt.Circle((vertices[0].x,  vertices[0].y), radius, fc="blue", label="unus")
plt.gca().add_patch(circle1)
circle = MoveableCircle(circle1, vertices, vertex_text, lines)
circle.connect()
circles.append(circle)

circle2 = plt.Circle((vertices[1].x,  vertices[1].y), radius, fc="blue", label="duo")
plt.gca().add_patch(circle2)
circle = MoveableCircle(circle2, vertices, vertex_text, lines)
circle.connect()
circles.append(circle)

circle3 = plt.Circle((vertices[2].x,  vertices[2].y), radius, fc="blue", label="tres")
plt.gca().add_patch(circle3)
circle = MoveableCircle(circle3, vertices, vertex_text, lines)
circle.connect()
circles.append(circle)


##########################  vertex_text 1,2,3  #########################################
#  2. Draw vertex text

text = Vertex_text(vertices[0].x, vertices[0].y)
vertex_text1 = plt.text(0.01, 0.98, text, fontsize=font_size, transform=axes.transAxes)
vertex_text.append(vertex_text1)

text = Vertex_text(vertices[1].x, vertices[1].y)
vertex_text2 = plt.text(0.93, 0.98, text, fontsize=font_size, transform=axes.transAxes)
vertex_text.append(vertex_text2)

text = Vertex_text(vertices[2].x, vertices[2].y)
vertex_text3 = plt.text(0.46, 0.05, text, fontsize=font_size, transform=axes.transAxes)
vertex_text.append(vertex_text3)


#########################  lines 1,2,3  ############################################
#  3.  Draw exterior lines
line1 = plt.Line2D([u.x, v.x],[u.y, v.y], color='black', linewidth = 4)
plt.gca().add_line(line1)
lines.append(line1)

line2 = plt.Line2D([v.x, w.x],[v.y, w.y], color='black', linewidth = 4)
plt.gca().add_line(line2)
lines.append(line2)

line3 = plt.Line2D([w.x, u.x],[w.y, u.y], color='black', linewidth = 4)
plt.gca().add_line(line3)
lines.append(line3)


#########################  interior angles 1,2,3  ###################################
#  4.  Get interior angles
angle = GetInteriorAngle(0,2)
text = f'Theta13 = {angle:.2f}'
interior_angles_text1 = plt.text(0.01, 0.94, text, fontsize=font_size, transform=axes.transAxes)
interior_angles_text.append(interior_angles_text1)

angle = GetInteriorAngle(1, 0)
text = f'Theta21 = {angle:.2f}'
interior_angles_text1 = plt.text(0.88, 0.94, text, fontsize=font_size, transform=axes.transAxes)
interior_angles_text.append(interior_angles_text1)

angle = GetInteriorAngle(2, 1)
text = f'Theta32 = {angle:.2f}'
interior_angles_text1 = plt.text(0.46, 0.01, text, fontsize=font_size, transform=axes.transAxes)
interior_angles_text.append(interior_angles_text1)





plt.show()