import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import time

fig = plt.figure()
ax = fig.add_subplot(projection='polar')
xs = []
ys = []
radar_vals = dict()
invalid = False


# This function is called periodically from FuncAnimation
serialPort = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)

def animate(i, xs, ys):
    serialPort.write(b's')
    data = serialPort.readline()
    try:
	    data = data.decode('ascii')
	    data = list(eval(data))

    except:
    	return

    if type(data[0]) == int:
        radar_vals[data[0]] = float(data[1])
        print('recieved : ', data[0], " : ", data[1])
    else:
        radar_vals[data[1]] = float(data[0])
        print('recieved : ', data[1], " : ", data[0])
    xs = list(radar_vals.keys())
    ys = list(radar_vals.values())

    ax.clear()
    ax.scatter(xs, ys)
    plt.title('RADAR values')
    ax.set_thetamin(0)
    ax.set_thetamax(180)
    plt.ylabel('Distance')
    plt.xlabel('Angle')


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
