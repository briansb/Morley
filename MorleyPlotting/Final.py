# https://matplotlib.org/3.1.0/users/event_handling.html

####  Plan  ####
#  1.  Draw circles
#  2.  Draw vertex text
#  3.  Draw exterior lines
#  4.  Compute interior angles
#  5.  Compute exerior angles
#  6.  Compute slope, y-intercept of interior lines
#  7.  Compute intersection of lines

#  9.  Draw lines from vertices to inner points, ie, 
#            plot lines 4 - 9
# 10.  Draw one line connecting inner points
# 11.  Compute side lengths of inner triangle

#  Then, on_motion, re-draw everybody


from ast import AsyncFunctionDef
import pdb
import math
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from numpy import inner

pi = math.acos(-1.0)
radian_to_degrees = 360.0 / (2.0 * pi)

def get_vertex_text(point, x, y):
    return f'{point} = ({x:.1f},{y:.1f})'

def get_interior_angle(index):
    if index == 1:    # get two vectors from vertex1 and compute dot product
        vector1_x = v.x - u.x
        vector1_y = v.y - u.y
        vector2_x = w.x - u.x
        vector2_y = w.y - u.y
    elif index == 2: 
        vector1_x = u.x - v.x
        vector1_y = u.y - v.y
        vector2_x = w.x - v.x
        vector2_y = w.y - v.y
    elif index == 3:  
        vector1_x = u.x - w.x
        vector1_y = u.y - w.y
        vector2_x = v.x - w.x
        vector2_y = v.y - w.y

    dot_product = vector1_x*vector2_x + vector1_y*vector2_y
    mag1 = math.sqrt(vector1_x*vector1_x + vector1_y*vector1_y)
    mag2 = math.sqrt(vector2_x*vector2_x + vector2_y*vector2_y)
    cosine_theta = dot_product/(mag1 * mag2)
    angle = math.acos(cosine_theta) * radian_to_degrees
    return angle

def get_interior_angle_text(i):
    angle = get_interior_angle(i)
    return f'Interior angle = {angle:.1f}'

def get_exterior_angle(index):
    if index == 1:    # get two vectors from vertex1 and compute dot product
        slope = (v.y - u.y) / (v.x - u.x)
    elif index == 2: 
        slope = (w.y - v.y) / (w.x - v.x)
    elif index == 3:  
        slope = (u.y - w.y) / (u.x - w.x)

    angle = math.atan(slope) * radian_to_degrees
    return angle

def get_exterior_angle_text(i):
    angle = get_exterior_angle(i)
    return f'Off-horizontal angle = {angle:.1f}'

def get_interior_line(index):
    if index == 4:
        angle = get_exterior_angle(1) - (get_interior_angle(1) / 3.0)
    if index == 5:
        angle = get_exterior_angle(1) - (2.0 * get_interior_angle(1) / 3.0)
    if index == 6:
        angle = get_exterior_angle(2) - (get_interior_angle(2) / 3.0)
    if index == 7:
        angle = get_exterior_angle(2) - (2.0 * get_interior_angle(2) / 3.0)
    if index == 8:
        angle = get_exterior_angle(3) - (get_interior_angle(3) / 3.0)
    if index == 9:
        angle = get_exterior_angle(3) - (2.0 * get_interior_angle(3) / 3.0)

    if index == 4 or index == 5:
        x_pt = u.x
        y_pt = u.y
    if index == 6 or index == 7:
        x_pt = v.x
        y_pt = v.y
    if index == 8 or index == 9:
        x_pt = w.x
        y_pt = w.y

    slope = math.tan(angle/radian_to_degrees)
    y_intercept = y_pt - (slope * x_pt)
    return slope, y_intercept

def get_interior_line_text(i):
    slope, intercept = get_interior_line(i)
    return f'   line{i}, {slope:.2f},{intercept:.1f}'

def get_line_intersection(i,j):
    slope_i, intercept_i = get_interior_line(i)
    slope_j, intercept_j = get_interior_line(j)
    final_x = (intercept_j - intercept_i) / (slope_i - slope_j)
    final_y = (slope_i * final_x) + intercept_i
    return final_x, final_y

def get_line_intersection_text(index, i, j):
    x_final, y_final = get_line_intersection(i,j)
    return f'Inner vertex{index} = {x_final:.1f},{y_final:.1f}'

def redraw_line(i, j, x, y):
    xdata = lines[i].get_xdata()
    ydata = lines[i].get_ydata()
    xdata[1] = x
    ydata[1] = y
    lines[i].set_xdata(xdata)
    lines[i].set_ydata(ydata)

    xdata = lines[j].get_xdata()
    ydata = lines[j].get_ydata()
    xdata[0] = x
    ydata[0] = y
    lines[j].set_xdata(xdata)
    lines[j].set_ydata(ydata)

def redraw_interior_line(index, i, j, x, y):
    pt_x, pt_y = get_line_intersection(i,j)
    x_data = [x, pt_x]
    y_data = [y, pt_y]
    lines[index].set_xdata(x_data)
    lines[index].set_ydata(y_data)

def redraw_inner_line():
    x1, y1 = get_line_intersection(4,7)
    x2, y2 = get_line_intersection(6,9)
    x3, y3 = get_line_intersection(5,8)
    x_data = [x1,x2,x3,x1]
    y_data = [y1,y2,y3,y1]  
    inner_line.set_xdata(x_data)
    inner_line.set_ydata(y_data)

def get_inner_side_length(index1, index2):
    if index1 == 1 and index2 == 2:
        x1, y1 = get_line_intersection(4,7)
        x2, y2 = get_line_intersection(6,9)
    if index1 == 2 and index2 == 3:
        x1, y1 = get_line_intersection(6,9)
        x2, y2 = get_line_intersection(5,8)
    if index1 == 3 and index2 == 1:
        x1, y1 = get_line_intersection(5,8)
        x2, y2 = get_line_intersection(4,7)

    length = math.sqrt((y2-y1)*(y2-y1) + (x2-x1)*(x2-x1))
    return length

def get_inner_side_length_text(index1, index2):
    length = get_inner_side_length(index1, index2)
    return f'Side length {index1}-{index2} = {length:.2f}'

class Point(object):
    def __init__(self, x, y):
        self.x = x
        self.y = y

class MoveableCircle(object):
    def __init__(self, circle):
        self.circle = circle
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
        # x and y are the new coordinates of the circle just moved...use them
        # 1. Re-draw circle
        self.circle.center = (x, y)

        # identify index of circle that was moved and set u, v, or w
        if self.circle.get_label() == "unus":
            index = 1
            point = 'u'
            u.x = x
            u.y = y
        elif self.circle.get_label() == "duo":
            index = 2
            point = 'v'
            v.x = x
            v.y = y
        elif self.circle.get_label() == "tres":
            index = 3
            point = 'w'
            w.x = x
            w.y = y

        #  2.  Re-draw vertex text
        text = get_vertex_text(point, x, y)
        vertex_text[index].set_text(text)

        #  3.  Re-draw exterior lines
        if index == 1:    # re-draw lines 3 and 1
            # x, y are the new end point of line 3
            # x, y are the new beginning point of line 1
            redraw_line(3, 1, x, y)
        elif index == 2:  # re-draw lines 1 and 2
            redraw_line(1, 2, x, y)
        elif index == 3:  # re-draw lines 2 and 3
            redraw_line(2, 3, x, y)

        #  Intermediate calculations
        #  4.  Re-compute interior angles
        for i in range(1,4):
            text = get_interior_angle_text(i)
            interior_angle_text[i].set_text(text)

        #  5.  Re-compute exterior angles
        for i in range(1,4):
            text = get_exterior_angle_text(i)
            exterior_angle_text[i].set_text(text)

        #  6.  Compute slope, y-intercept of interior lines
        text = get_interior_line_text(4)
        interior_line_text[4].set_text(text)
        text = get_interior_line_text(5)
        interior_line_text[5].set_text(text)
        text = get_interior_line_text(6)
        interior_line_text[6].set_text(text)
        text = get_interior_line_text(7)
        interior_line_text[7].set_text(text)
        text = get_interior_line_text(8)
        interior_line_text[8].set_text(text)
        text = get_interior_line_text(9)
        interior_line_text[9].set_text(text)

        #  7.  Compute intersection of lines
        text = get_line_intersection_text(1, 4,7)
        line_intersection_text[1].set_text(text)
        text = get_line_intersection_text(2, 6,9)
        line_intersection_text[2].set_text(text)
        text = get_line_intersection_text(3, 5,8)
        line_intersection_text[3].set_text(text)

        #  9.  Re-draw lines 4 - 9, the interior lines
        if index == 1:    # re-draw lines 4 and 5
            redraw_interior_line(4, 4, 7, x, y)
            redraw_interior_line(5, 5, 8, x, y)
            redraw_interior_line(6, 6, 9, v.x, v.y)
            redraw_interior_line(7, 4, 7, v.x, v.y)
            redraw_interior_line(8, 5, 8, w.x, w.y)
            redraw_interior_line(9, 6, 9, w.x, w.y)
        elif index == 2:  # re-draw lines 6 and 7
            redraw_interior_line(4, 4, 7, u.x, u.y)
            redraw_interior_line(5, 5, 8, u.x, u.y)
            redraw_interior_line(6, 6, 9, x, y)
            redraw_interior_line(7, 4, 7, x, y)
            redraw_interior_line(8, 5, 8, w.x, w.y)
            redraw_interior_line(9, 6, 9, w.x, w.y)
        elif index == 3:  # re-draw lines 8 and 9
            redraw_interior_line(4, 4, 7, u.x, u.y)
            redraw_interior_line(5, 5, 8, u.x, u.y)
            redraw_interior_line(6, 6, 9, v.x, v.y)
            redraw_interior_line(7, 4, 7, v.x, v.y)
            redraw_interior_line(8, 5, 8, x, y)
            redraw_interior_line(9, 6, 9, x, y)

        # 10.  Re-draw inner line
        redraw_inner_line()

        # 11.  Compute side lengths of inner triangle
        text = get_inner_side_length_text(1,2)
        inner_side_length_text[1].set_text(text)
        text = get_inner_side_length_text(2,3)
        inner_side_length_text[2].set_text(text)
        text = get_inner_side_length_text(3,1)
        inner_side_length_text[3].set_text(text)



        self.circle.figure.canvas.draw()
    ######  end of on_motion event  ##################

    

##################################   Main    ######################################

# the None starting value is to avoid dealing with 0-index
# these values get updated on motion
circles = [None]        # circles are plt.Circle()
vertex_text = [None]    # vertex_text are plt.text
lines = [None]          # lines are the exterior (1-3) and interior lines (4-9)
interior_angle_text = [None]  # interior angle of each vertex
exterior_angle_text = [None]  # angle of exterior lines with x-axis
interior_line_text = [None]   # slope and y-intercept for interior lines
line_intersection_text = [None]  # the three inner triangle point as text
inner_vertices = [None]          # the three inner triangle points
inner_side_length_text = [None]  # length of sides of inner triangle

fig = plt.figure(figsize=(16,10))
axes = plt.axes()
axes.set_xlim([-6,10])
axes.set_ylim([-4,6])
# for testing with Plot 2
# axes.set_xlim([-16,36])
# axes.set_ylim([-6,26])
font_size = 12
radius = 0.25

# set the three vertices
u = Point(-2, 4)
v = Point(6, 2)
w = Point(0, -1)

###########################  circles 1,2,3 ######################################################
#  1. Draw circles

circle1 = plt.Circle((u.x,  u.y), radius, fc="blue", label="unus")
plt.gca().add_patch(circle1)
circle = MoveableCircle(circle1)
circle.connect()
circles.append(circle)

circle2 = plt.Circle((v.x,  v.y), radius, fc="blue", label="duo")
plt.gca().add_patch(circle2)
circle = MoveableCircle(circle2)
circle.connect()
circles.append(circle)

circle3 = plt.Circle((w.x,  w.y), radius, fc="blue", label="tres")
plt.gca().add_patch(circle3)
circle = MoveableCircle(circle3)
circle.connect()
circles.append(circle)


##########################  vertex_text 1,2,3  #########################################
#  2. Draw vertex text

text = get_vertex_text('u', u.x, u.y)
vertex_text1 = plt.text(0.01, 0.98, text, fontsize=font_size, transform=axes.transAxes)
vertex_text.append(vertex_text1)

text = get_vertex_text('v', v.x, v.y)
vertex_text2 = plt.text(0.80, 0.98, text, fontsize=font_size, transform=axes.transAxes)
vertex_text.append(vertex_text2)

text = get_vertex_text('w', w.x, w.y)
vertex_text3 = plt.text(0.46, 0.17, text, fontsize=font_size, transform=axes.transAxes)
vertex_text.append(vertex_text3)


#########################  lines 1,2,3  ############################################
#  3.  Draw exterior lines
line1 = plt.Line2D([u.x, v.x],[u.y, v.y], color='black', linewidth = 4)
plt.gca().add_line(line1)
lines.append(line1)
interior_line_text.append(None)  # will never use these

line2 = plt.Line2D([v.x, w.x],[v.y, w.y], color='black', linewidth = 4)
plt.gca().add_line(line2)
lines.append(line2)
interior_line_text.append(None)

line3 = plt.Line2D([w.x, u.x],[w.y, u.y], color='black', linewidth = 4)
plt.gca().add_line(line3)
lines.append(line3)
interior_line_text.append(None)


#########################  intermediate calculations   ###############################
#  4.  Compute interior angles
text = get_interior_angle_text(1)
interior_angle_text1 = plt.text(0.01, 0.95, text, fontsize=font_size, transform=axes.transAxes)
interior_angle_text.append(interior_angle_text1)

text = get_interior_angle_text(2)
interior_angle_text2 = plt.text(0.80, 0.95, text, fontsize=font_size, transform=axes.transAxes)
interior_angle_text.append(interior_angle_text2)

text = get_interior_angle_text(3)
interior_angle_text3 = plt.text(0.46, 0.14, text, fontsize=font_size, transform=axes.transAxes)
interior_angle_text.append(interior_angle_text3)

#  5.  Compute exterior angles
text = get_exterior_angle_text(1)
exterior_angle_text1 = plt.text(0.01, 0.92, text, fontsize=font_size, transform=axes.transAxes)
exterior_angle_text.append(exterior_angle_text1)

text = get_exterior_angle_text(2)
exterior_angle_text2 = plt.text(0.80, 0.92, text, fontsize=font_size, transform=axes.transAxes)
exterior_angle_text.append(exterior_angle_text2)

text = get_exterior_angle_text(3)
exterior_angle_text3 = plt.text(0.46, 0.11, text, fontsize=font_size, transform=axes.transAxes)
exterior_angle_text.append(exterior_angle_text3)

#  6.  Compute slope, y-intercept of interior lines
plt.text(0.01, 0.89, 'Slope, y-intercept', fontsize=font_size, transform=axes.transAxes)
text = get_interior_line_text(4)
interior_line_text4 = plt.text(0.01, 0.86, text, fontsize=font_size, transform=axes.transAxes)
interior_line_text.append(interior_line_text4)
text = get_interior_line_text(5)
interior_line_text5 = plt.text(0.01, 0.83, text, fontsize=font_size, transform=axes.transAxes)
interior_line_text.append(interior_line_text5)

plt.text(0.80, 0.89, 'Slope, y-intercept', fontsize=font_size, transform=axes.transAxes)
text = get_interior_line_text(6)
interior_line_text6 = plt.text(0.80, 0.86, text, fontsize=font_size, transform=axes.transAxes)
interior_line_text.append(interior_line_text6)
text = get_interior_line_text(7)
interior_line_text7 = plt.text(0.80, 0.83, text, fontsize=font_size, transform=axes.transAxes)
interior_line_text.append(interior_line_text7)

plt.text(0.46, 0.08, 'Slope, y-intercept', fontsize=font_size, transform=axes.transAxes)
text = get_interior_line_text(8)
interior_line_text8 = plt.text(0.46, 0.05, text, fontsize=font_size, transform=axes.transAxes)
interior_line_text.append(interior_line_text8)
text = get_interior_line_text(9)
interior_line_text9 = plt.text(0.46, 0.02, text, fontsize=font_size, transform=axes.transAxes)
interior_line_text.append(interior_line_text9)

##################  line intersections  #############################################
#  7.  Compute intersection of lines
text = get_line_intersection_text(1, 4,7)
line_intersection_text_4_7 = plt.text(0.46, 0.98, text, fontsize=font_size, transform=axes.transAxes)
line_intersection_text.append(line_intersection_text_4_7)

text = get_line_intersection_text(2, 6,9)
line_intersection_text_6_9 = plt.text(0.80, 0.4, text, fontsize=font_size, transform=axes.transAxes)
line_intersection_text.append(line_intersection_text_6_9)

text = get_line_intersection_text(3, 5,8)
line_intersection_text_5_8 = plt.text(0.01, 0.4, text, fontsize=font_size, transform=axes.transAxes)
line_intersection_text.append(line_intersection_text_5_8)


#########################  lines 4 - 9  ############################################
#  9.  Draw lines from vertices to inner points
inner_vertex = get_line_intersection(4,7)
line4 = plt.Line2D([u.x, inner_vertex[0]],[u.y, inner_vertex[1]], color='red', linewidth = 2)
plt.gca().add_line(line4)
lines.append(line4)
inner_vertex = get_line_intersection(5,8)
line5 = plt.Line2D([u.x, inner_vertex[0]],[u.y, inner_vertex[1]], color='red', linewidth = 2)
plt.gca().add_line(line5)
lines.append(line5)
inner_vertex = get_line_intersection(6,9)
line6 = plt.Line2D([v.x, inner_vertex[0]],[v.y, inner_vertex[1]], color='red', linewidth = 2)
plt.gca().add_line(line6)
lines.append(line6)
inner_vertex = get_line_intersection(4,7)
line7 = plt.Line2D([v.x, inner_vertex[0]],[v.y, inner_vertex[1]], color='red', linewidth = 2)
plt.gca().add_line(line7)
lines.append(line7)
inner_vertex = get_line_intersection(5,8)
line8 = plt.Line2D([w.x, inner_vertex[0]],[w.y, inner_vertex[1]], color='red', linewidth = 2)
plt.gca().add_line(line8)
lines.append(line8)
inner_vertex = get_line_intersection(6,9)
line9 = plt.Line2D([w.x, inner_vertex[0]],[w.y, inner_vertex[1]], color='red', linewidth = 2)
plt.gca().add_line(line9)
lines.append(line9)

#########################   Inner line  #######################################
# 10.  Draw one line connecting inner points
x1, y1 = get_line_intersection(4,7)
x2, y2 = get_line_intersection(6,9)
x3, y3 = get_line_intersection(5,8)
inner_line = plt.Line2D([x1,x2,x3,x1],[y1,y2,y3,y1],color='black', linewidth=2)
plt.gca().add_line(inner_line)

#########################  Length of inner sides
# 11.  Compute side lengths of inner triangle
text = get_inner_side_length_text(1,2)
inner_side_length_text1 = plt.text(0.46, 0.95, text, fontsize=font_size, transform=axes.transAxes)
inner_side_length_text.append(inner_side_length_text1)
text = get_inner_side_length_text(2,3)
inner_side_length_text2 = plt.text(0.80, 0.37, text, fontsize=font_size, transform=axes.transAxes)
inner_side_length_text.append(inner_side_length_text2)
text = get_inner_side_length_text(3,1)
inner_side_length_text3 = plt.text(0.01, 0.37, text, fontsize=font_size, transform=axes.transAxes)
inner_side_length_text.append(inner_side_length_text3)


plt.show()