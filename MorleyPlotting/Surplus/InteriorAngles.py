# https://matplotlib.org/3.1.0/users/event_handling.html

import pdb
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
pi = math.acos(-1.0)
radian_to_degrees = 360.0 / (2.0 * pi)

def GetInteriorAngle(line1, line2):
    vec1x = line1.get_xdata()[1] - line1.get_xdata()[0]
    vec1y = line1.get_ydata()[1] - line1.get_ydata()[0]
    vec2x = line2.get_xdata()[0] - line2.get_xdata()[1]
    vec2y = line2.get_ydata()[0] - line2.get_ydata()[1]
    dot_product = (vec1x * vec2x) + (vec1y * vec2y)
    vec1_mag = math.sqrt((vec1x*vec1x) + (vec1y*vec1y))
    vec2_mag = math.sqrt((vec2x*vec2x) + (vec2y*vec2y))
    cos_theta = dot_product / (vec1_mag * vec2_mag)
    theta = math.acos(cos_theta)
    return theta * radian_to_degrees

def ComputeSlopeAndInterceptFromTwoPoints(y2, y1, x2, x1):
    slope = (y2 - y1) / (x2 - x1)
    intercept = y1 - x1 * slope
    return slope, intercept

class MoveableCircle(object):
    def __init__(self, circle, lines, vertices, interior_angles, equations):
        self.circle = circle
        self.lines = lines
        self.vertices = vertices
        self.interior_angles = interior_angles
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
        elif self.circle.get_label() == "duo":
            self.redraw_exterior_lines(event, x0, y0, dx, dy, 1, 0)
            self.redraw_vertex_text(event, 1)
            self.recompute_line_equation(event, 1, 0)
        elif self.circle.get_label() == "tres":
            self.redraw_exterior_lines(event, x0, y0, dx, dy, 2, 1)
            self.redraw_vertex_text(event, 2)
            self.recompute_line_equation(event, 2, 1)
        else:
            print("Should not be here - statement 1")

        # when the circle moves, if affects all interior lines
        self.recompute_interior_angles(event)

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

    def redraw_vertex_text(self, event, i):
        newx, newy = self.circle.center
        if self.circle.get_label() == "unus" or self.circle.get_label() == "duo":
            newy = newy + y_offset
        elif self.circle.get_label() == "tres":
            newy = newy - y_offset
        self.vertices[i].set_x(newx)
        self.vertices[i].set_y(newy)
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

    def recompute_interior_angles(self, event):
        angle = GetInteriorAngle(self.lines[0], self.lines[2])
        text = f'Theta13 = {angle:.1f}'
        self.interior_angles[0].set_text(text)
        angle = GetInteriorAngle(self.lines[1], self.lines[0])
        text = f'Theta13 = {angle:.1f}'
        self.interior_angles[1].set_text(text)
        angle = GetInteriorAngle(self.lines[2], self.lines[1])
        text = f'Theta13 = {angle:.1f}'
        self.interior_angles[2].set_text(text)


##################################   Main    ######################################
fig = plt.figure(figsize=(16,10))
axes = plt.axes()
axes.set_xlim([-2,14])
axes.set_ylim([-2,8])
# for testing with Plot 2
# axes.set_xlim([-16,36])
# axes.set_ylim([-6,26])
font_size = 12
x_min, x_max = axes.get_xlim()
x_offset = 0.15 * (x_max - x_min)
y_min, y_max = axes.get_ylim()
y_offset = 0.05 * (y_max - y_min)
x_mid = (x_max - x_min) / 2.0
y_mid = (y_max - y_min) / 2.0


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
interior_angles = []
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
vertex1 = plt.text(ux, uy + y_offset, text, fontsize=font_size)
vertices.append(vertex1)

text = f'({vx:.1f},{vy:.1f})'
vertex2 = plt.text(vx, vy + y_offset, text, fontsize=font_size)
vertices.append(vertex2)

text = f'({wx:.1f},{wy:.1f})'
vertex3 = plt.text(wx, wy - y_offset, text, fontsize=font_size)
vertices.append(vertex3)

###########################  interior angles ###############################################

angle = GetInteriorAngle(line1, line3)
text = f'Theta13 = {angle:.1f}'
interior_angle1 = plt.text(0.02, 0.95, text, fontsize=font_size, transform=axes.transAxes)
interior_angles.append(interior_angle1)

slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(vy, uy, vx, ux)
alpha1 = math.atan(slope) * radian_to_degrees
alpha4 = alpha1 - angle/3.0
text = f'Alpha4 = {alpha4:.1f}'
interior_angle4 = plt.text(0.02, 0.90, text, fontsize=font_size, transform=axes.transAxes)
alpha5 = alpha1 - 2.0*angle/3.0
text = f'Alpha5 = {alpha5:.1f}'
interior_angle5 = plt.text(0.02, 0.85, text, fontsize=font_size, transform=axes.transAxes)


angle = GetInteriorAngle(line2, line1)
text = f'Theta21 = {angle:.1f}'
interior_angle2 = plt.text(0.88, 0.95, text, fontsize=font_size, transform=axes.transAxes)
interior_angles.append(interior_angle2)

angle = GetInteriorAngle(line3, line2)
text = f'Theta23 = {angle:.1f}'
interior_angle3 = plt.text(0.45, 0.03, text, fontsize=font_size, transform=axes.transAxes)
interior_angles.append(interior_angle3)

interior_angles.append(interior_angle4)
interior_angles.append(interior_angle5)

###########################  equations 1,2,3   ###############################################

slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(vy, uy, vx, ux)
angle = math.atan(slope) * radian_to_degrees
line_eqn = f"y = {slope:.2f}x({angle:.1f}) + {intercept:.2f}"
equation1 = plt.text(0.5, 0.95, line_eqn, fontsize=font_size, transform=axes.transAxes)
equations.append(equation1)

slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(wy, vy, wx, vx)
angle = math.atan(slope) * radian_to_degrees
line_eqn = f"y = {slope:.2f}x({angle:.1f}) + {intercept:.2f}"
equation2 = plt.text(0.83, 0.25, line_eqn, fontsize=font_size, transform=axes.transAxes)
equations.append(equation2)

slope, intercept = ComputeSlopeAndInterceptFromTwoPoints(uy, wy, ux, wx)
angle = math.atan(slope) * radian_to_degrees
line_eqn = f"y = {slope:.2f}x({angle:.1f}) + {intercept:.2f}"
equation3 = plt.text(0.02, 0.25, line_eqn, fontsize=font_size, transform=axes.transAxes)
equations.append(equation3)

###########################  circles 1,2,3 ######################################################

circle1 = plt.Circle((ux, uy), radius, fc="blue", label="unus")
plt.gca().add_patch(circle1)
circle = MoveableCircle(circle1, lines, vertices, interior_angles, equations)
circle.connect()
circles.append(circle)

circle2 = plt.Circle((vx, vy), radius, fc="blue", label="duo")
plt.gca().add_patch(circle2)
circle = MoveableCircle(circle2, lines, vertices, interior_angles, equations)
circle.connect()
circles.append(circle)

circle3 = plt.Circle((wx, wy), radius, fc="blue", label="tres")
plt.gca().add_patch(circle3)
circle = MoveableCircle(circle3, lines, vertices, interior_angles, equations)
circle.connect()
circles.append(circle)

plt.show()