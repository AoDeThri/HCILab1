import random

import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

plt.style.use('dark_background')

fig = plt.figure()
ax = plt.axes(xlim=(-50, 50), ylim=(-50, 50))
line, = ax.plot([], [], lw=2)


# initialization function
def init():
    # creating an empty plot/frame
    line.set_data([], [])
    return line,


# lists to store x and y axis points
xdata, ydata = [], []


# simulate ghost effect of oscilloscope
def ghostImage(x, y):
    xdata.append(x)
    ydata.append(y)
    if len(xdata) > 60:
        del xdata[0]
        del ydata[0]
    return xdata, ydata


# animation function
def animate(i):
    # t is a parameter
    t = i / 100.0

    # x, y values to be plotted
    x = 40 * np.sin(2 * 2 * np.pi * (t + 0.3))
    y = 40 * np.cos(3 * 2 * np.pi * t)

    # appending new points to x, y axes points list

    line.set_data(ghostImage(x, y))
    return line,


# hiding the axis details
plt.axis('off')

# call the animator
anim = animation.FuncAnimation(fig, animate, init_func=init,
                               frames=1000, interval=20, blit=True)

# save the animation as gif file
anim.save('figure.gif', writer='imagemagick')