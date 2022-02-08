# https://matplotlib.org/3.1.0/users/event_handling.html

import pdb
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.artist import Artist
import numpy as np

# # First example
# fig, ax = plt.subplots()
# ax.plot(np.random.rand(10))

# def onclick(event):
#     print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#           ('double' if event.dblclick else 'single', event.button,
#            event.x, event.y, event.xdata, event.ydata))

# cid = fig.canvas.mpl_connect('button_press_event', onclick)
# plt.show()


# # Second example
# class LineBuilder:
#     def __init__(self, line):
#         self.line = line
#         self.xs = list(line.get_xdata())
#         self.ys = list(line.get_ydata())
#         self.cid = line.figure.canvas.mpl_connect('button_press_event', self)
#         print("end of __init__")

#     def __call__(self, event):
#         print('click', event)
#         if event.inaxes!=self.line.axes: return
#         # it re-draws the whole thing
#         self.xs.append(event.xdata)
#         self.ys.append(event.ydata)
#         self.line.set_data(self.xs, self.ys)
#         self.line.figure.canvas.draw()
        
#         # these two statments remove the previous points
#         del self.xs[0]
#         del self.ys[0]
#         #print(event.xdata)
#         print(self.xs[:])

# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_title('click to build line segments')
# line, = ax.plot([0], [0])  # empty line
# linebuilder = LineBuilder(line)
# plt.show()


# Third example
# https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.patches.Rectangle.html#matplotlib.patches.Rectangle

class DraggableRectangle(object):
    def __init__(self, rect, line):
        self.rect = rect
        self.line = line
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.rect.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.rect.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.rect.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.rect.axes: return
        contains, attrd = self.rect.contains(event)
        if not contains: return
        print('on_press x0, y0 = ', self.rect.xy)
        print('\tmouse at ', event.xdata, event.ydata)
        # x0, y0 are lower left coordinates of rectangle
        x0, y0 = self.rect.xy
        # event.xdata, .ydata are coordinates of mouse when pressed
        self.press = x0, y0, event.xdata, event.ydata

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.rect.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will move the rect if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.rect.axes: return
        x0, y0, xpress, ypress = self.press
        print('on_motion x0, y0 - ', x0, y0)
        print('\tmouse at ', event.xdata, event.ydata)
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        self.rect.set_x(x0+dx)
        self.rect.set_y(y0+dy)
        linex = self.line.get_xdata()
        self.line.set_xdata([linex[0], linex[1] + dx])
        self.rect.figure.canvas.draw()
        self.line.figure.canvas.draw()


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.rect.figure.canvas.mpl_disconnect(self.cidpress)
        self.rect.figure.canvas.mpl_disconnect(self.cidrelease)
        self.rect.figure.canvas.mpl_disconnect(self.cidmotion)


fig = plt.figure(figsize=(12,6))
axes = plt.axes()
axes.set_xlim([-1,12])
axes.set_ylim([-1,6])

drs = []
# rects = plt.bar(range(3), 10*np.random.rand(3))
# for rect in rects:

#     dr = DraggableRectangle(rect)
#     dr.connect()
#     drs.append(dr)

line1 = plt.Line2D((4, 5), (4, 5.9), color='green', linewidth = 4)
plt.gca().add_line(line1)
#plt.axis('scaled')

rectangle1 = plt.Rectangle((0,0), 5, 2, fc='yellow',ec="red")
plt.gca().add_patch(rectangle1)
#plt.axis('scaled')
dr = DraggableRectangle(rectangle1, line1)
dr.connect()
drs.append(dr)

rectangle2 = plt.Rectangle((1,4), 1, 1, fc='black',ec="red")
plt.gca().add_patch(rectangle2)
#plt.axis('scaled')
dr = DraggableRectangle(rectangle2, line1)
dr.connect()
drs.append(dr)

circle = plt.Circle((8,4),1.5, fc='red',ec="red")
plt.gca().add_patch(circle)
#plt.axis('scaled')



plt.show()