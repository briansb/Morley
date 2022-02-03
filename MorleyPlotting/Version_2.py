import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse

# https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.patches.Ellipse.html#matplotlib.patches.Ellipse
# https://matplotlib.org/3.1.0/api/_as_gen/matplotlib.patches.Circle.html#matplotlib.patches.Circle
class DraggableCircle:
    def __init__(self, circ):
        self.circ = circ
        self.press = None

    def connect(self):
        'connect to all the events we need'
        self.cidpress = self.circ.figure.canvas.mpl_connect(
            'button_press_event', self.on_press)
        self.cidrelease = self.circ.figure.canvas.mpl_connect(
            'button_release_event', self.on_release)
        self.cidmotion = self.circ.figure.canvas.mpl_connect(
            'motion_notify_event', self.on_motion)

    def on_press(self, event):
        'on button press we will see if the mouse is over us and store some data'
        if event.inaxes != self.circ.axes: return
        contains, attrd = self.circ.contains(event)
        if not contains: return
        print('event contains', self.circ.center)
        x0, y0 = self.circ.center
        self.press = x0, y0, event.xdata, event.ydata

    def on_release(self, event):
        'on release we reset the press data'
        self.press = None
        self.circ.figure.canvas.draw()

    def on_motion(self, event):
        'on motion we will move the circle if the mouse is over us'
        if self.press is None: return
        if event.inaxes != self.circ.axes: return
        x0, y0, xpress, ypress = self.press
        dx = event.xdata - xpress
        dy = event.ydata - ypress
        #print('x0=%f, xpress=%f, event.xdata=%f, dx=%f, x0+dx=%f' %
        #      (x0, xpress, event.xdata, dx, x0+dx))
        #self.circ.set_x(x0+dx)
        #self.circ.set_y(y0+dy)
        xy = x0+dx, y0+dy
        self.circ._center = xy
        self.circ.figure.canvas.draw()


    def disconnect(self):
        'disconnect all the stored connection ids'
        self.circ.figure.canvas.mpl_disconnect(self.cidpress)
        self.circ.figure.canvas.mpl_disconnect(self.cidrelease)
        self.circ.figure.canvas.mpl_disconnect(self.cidmotion)





x = [5,7]
y = [4, 8]

fig, ax = plt.subplots()
# plt.xlim(0,10)
# plt.ylim(0,10)
# ax.plot(x, y, 'black', )

circs = [Ellipse((4,4),1,2,60)]

drs = []
for circ in circs:
    dr = DraggableCircle(circ)
    dr.connect()
    drs.append(dr)

plt.show()