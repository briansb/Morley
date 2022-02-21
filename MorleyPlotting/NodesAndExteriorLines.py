# https://matplotlib.org/3.1.0/users/event_handling.html

import pdb
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
pi = math.acos(-1.0)
radian_to_degrees = 360.0 / (2.0 * pi)

def ComputeSlopeAndInterceptFromTwoPoints(y2, y1, x2, x1):
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - x1 * slope
    return slope, intercept

class MoveableCircle(object):
    def __init__(self, circle, lines, vertices, equations):
        self.circle = circle
        self.lines = lines
        self.vertices = vertices
        self.equations = equations
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
            self.redraw_exterior_lines(event, x0, y0, dx, dy, 0, 2)
            self.redraw_vertex_text(event, 0)
            self.recompute_line_equation(event, 0, 2)
            # when the circle moves, if affects all interior lines
            self.redraw_interior_lines(event)
        elif self.circle.get_label() == "duo":
            self.redraw_exterior_lines(event, x0, y0, dx, dy, 1, 0)
            self.redraw_vertex_text(event, 1)
            self.recompute_line_equation(event, 1, 0)
            self.redraw_interior_lines(event)
        elif self.circle.get_label() == "tres":
            self.redraw_exterior_lines(event, x0, y0, dx, dy, 2, 1)
            self.redraw_vertex_text(event, 2)
            self.recompute_line_equation(event, 2, 1)
            self.redraw_interior_lines(event)
        else:
            print("Should not be here - statement 1")

        # re-draw the whole thing
        self.circle.figure.canvas.draw()
        #  end of on_motion event

    def redraw_exterior_lines(self, event, x0, y0, dx, dy, i, j):
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
        
    def redraw_interior_lines(self, event):
        return 3

    def redraw_vertex_text(self, event, i):
        newx, newy = self.circle.center
        text = f'({newx:.1f},{newy:.1f})'
        self.vertices[i].set_text(text)

    def recompute_line_equation(self, event, i, j):
        x = self.lines[i].get_xdata()
        y = self.lines[i].get_ydata()
        slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(y[1], y[0], x[1], x[0])
        angle = math.atan(slope) * radian_to_degrees
        line_eqn = f"y = {slope:.2f}x({angle:.1f}) + {intercept:.2f}"
        self.equations[i].set_text(line_eqn)

        x = self.lines[j].get_xdata()
        y = self.lines[j].get_ydata()
        slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(y[1], y[0], x[1], x[0])
        angle = math.atan(slope) * radian_to_degrees
        line_eqn = f"y = {slope:.2f}x({angle:.1f}) + {intercept:.2f}"
        self.equations[j].set_text(line_eqn)




##################################   Main    ######################################
fig = plt.figure(figsize=(16,10))
axes = plt.axes()
axes.set_xlim([-2,14])
axes.set_ylim([-2,8])
# for testing with Plot 2
# axes.set_xlim([-16,36])
# axes.set_ylim([-6,26])
font_size = 12


# initial values
ux = 2
uy = 5
vx = 10
vy = 3
wx = 4
wy = 0
radius = 0.25
lines = []                 # lines are plt.Line2D()
vertices = []              # vertices are plt.text()
circles = []               # circles are plt.Circle()
equations = []             # equations are plt.text()

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
vertex1 = plt.text(0 + 0.02, 1 - 0.03, text, fontsize=font_size, transform=axes.transAxes)
vertices.append(vertex1)

text = f'({vx:.1f},{vy:.1f})'
vertex2 = plt.text(1 - 0.17, 1 - 0.03, text, fontsize=font_size, transform=axes.transAxes)
vertices.append(vertex2)

text = f'({wx:.1f},{wy:.1f})'
vertex3 = plt.text(0.5 - 0.1, 0 + 0.04, text, fontsize=font_size, transform=axes.transAxes)
vertices.append(vertex3)

###########################  equations 1,2,3   ###############################################

slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(vy, uy, vx, ux)
angle = math.atan(slope) * radian_to_degrees
line_eqn = f"y = {slope:.2f}x({angle:.1f}) + {intercept:.2f}"
equation1 = plt.text(0 + 0.02, 1 - 0.06, line_eqn, fontsize=font_size, transform=axes.transAxes)
equations.append(equation1)

slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(wy, vy, wx, vx)
angle = math.atan(slope) * radian_to_degrees
line_eqn = f"y = {slope:.2f}x({angle:.1f}) + {intercept:.2f}"
equation2 = plt.text(1 - 0.17, 1 - 0.06, line_eqn, fontsize=font_size, transform=axes.transAxes)
equations.append(equation2)

slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(uy, wy, ux, wx)
angle = math.atan(slope) * radian_to_degrees
line_eqn = f"y = {slope:.2f}x({angle:.1f}) + {intercept:.2f}"
equation3 = plt.text(0.5 - 0.1, 0 + 0.01, line_eqn, fontsize=font_size, transform=axes.transAxes)
equations.append(equation3)

###########################  circles 1,2,3 ######################################################

circle1 = plt.Circle((ux, uy), radius, fc="blue", label="unus")
plt.gca().add_patch(circle1)
circle = MoveableCircle(circle1, lines, vertices, equations)
circle.connect()
circles.append(circle)

circle2 = plt.Circle((vx, vy), radius, fc="blue", label="duo")
plt.gca().add_patch(circle2)
circle = MoveableCircle(circle2, lines, vertices, equations)
circle.connect()
circles.append(circle)

circle3 = plt.Circle((wx, wy), radius, fc="blue", label="tres")
plt.gca().add_patch(circle3)
circle = MoveableCircle(circle3, lines, vertices, equations)
circle.connect()
circles.append(circle)

plt.show()