# https://matplotlib.org/3.1.0/users/event_handling.html

import pdb
import math
import matplotlib.pyplot as plt

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

def Vertex_text(x, y):
    return f'({x:.1f},{y:.1f})'

class MoveableCircle(object):
    def __init__(self, circle, points, vertices):
        self.circle = circle
        self.points = points
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
        self.circle.center = (x, y)

        # update u, v, w so that the new values are available to any item
        if self.circle.get_label() == "unus":
            index = 0
        elif self.circle.get_label() == "duo":
            index = 1
        elif self.circle.get_label() == "tres":
            index = 2
        
        self.points[index] = (x,y)
        #  1.  Update vertex text
        text = Vertex_text(x, y)
        self.vertices[index].set_text(text)
        #  2.  Update lines



        self.circle.figure.canvas.draw()
    ######  end of on_motion event  ##################


##################################   Main    ######################################
fig = plt.figure(figsize=(16,10))
axes = plt.axes()
axes.set_xlim([-2,14])
axes.set_ylim([-2,8])
# for testing with Plot 2
# axes.set_xlim([-16,36])
# axes.set_ylim([-6,26])
font_size = 12
radius = 0.25

# set the three points
u = Point(2, 5)
v = Point(10, 3)
w = Point(4, 0)
points = []
points.append(u)
points.append(v)
points.append(w)

circles = []        # circles are plt.Circle()
vertices = []       # vertices are plt.text


###########################  circles 1,2,3 ######################################################

circle1 = plt.Circle((points[0].x,  points[0].y), radius, fc="blue", label="unus")
plt.gca().add_patch(circle1)
circle = MoveableCircle(circle1, points, vertices)
circle.connect()
circles.append(circle)

circle2 = plt.Circle((points[1].x,  points[1].y), radius, fc="blue", label="duo")
plt.gca().add_patch(circle2)
circle = MoveableCircle(circle2, points, vertices)
circle.connect()
circles.append(circle)

circle3 = plt.Circle((points[2].x,  points[2].y), radius, fc="blue", label="tres")
plt.gca().add_patch(circle3)
circle = MoveableCircle(circle3, points, vertices)
circle.connect()
circles.append(circle)


##########################  vertices 1,2,3  #########################################

text = Vertex_text(points[0].x, points[0].y)
vertex1 = plt.text(0.01, 0.98, text, fontsize=font_size, transform=axes.transAxes)
vertices.append(vertex1)

text = Vertex_text(points[1].x, points[1].y)
vertex2 = plt.text(0.93, 0.98, text, fontsize=font_size, transform=axes.transAxes)
vertices.append(vertex2)

text = Vertex_text(points[2].x, points[2].y)
vertex3 = plt.text(0.47, 0.01, text, fontsize=font_size, transform=axes.transAxes)
vertices.append(vertex3)


#########################  lines 1,2,3  ############################################




plt.show()