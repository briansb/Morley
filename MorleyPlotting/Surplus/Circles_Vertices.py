# https://matplotlib.org/3.1.0/users/event_handling.html

####  Plan  ####
#  1. Draw circles
#  2. Draw vertex text
#  3. 



#  Then, on_motion, re-draw everybody


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
    def __init__(self, circle, vertices, vertex_text):
        self.circle = circle
        self.vertices = vertices
        self.vertex_text = vertex_text
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




        self.circle.figure.canvas.draw()
    ######  end of on_motion event  ##################


##################################   Main    ######################################

vertices = []       # u, v, and w
circles = []        # circles are plt.Circle()
vertex_text = []    # vertex_text are plt.text

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
circle = MoveableCircle(circle1, vertices, vertex_text)
circle.connect()
circles.append(circle)

circle2 = plt.Circle((vertices[1].x,  vertices[1].y), radius, fc="blue", label="duo")
plt.gca().add_patch(circle2)
circle = MoveableCircle(circle2, vertices, vertex_text)
circle.connect()
circles.append(circle)

circle3 = plt.Circle((vertices[2].x,  vertices[2].y), radius, fc="blue", label="tres")
plt.gca().add_patch(circle3)
circle = MoveableCircle(circle3, vertices, vertex_text)
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
vertex_text3 = plt.text(0.47, 0.01, text, fontsize=font_size, transform=axes.transAxes)
vertex_text.append(vertex_text3)




plt.show()