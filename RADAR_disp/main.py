import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import serial
import time

fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = []
ys = []
radar_vals = dict()
invalid = False


# This function is called periodically from FuncAnimation
def animate(i, xs, ys):
    time.sleep(0.09)
    serialPort = serial.Serial(port="/dev/ttyUSB0", baudrate=9600)
    data = serialPort.readline()
    try:
        data = data.decode('ascii')
        print(f"recieved {data}")
        data = eval(data)
        print(data)
    except:
        try:
            print("invalid data")
            if type(data) != str:
                data = data.decode('ascii')
            data = str(data)
            data = data + '}'
            data = eval(data)
        except:
            return
        print(data)

    if type(data) != dict:
        return

    radar_vals[list(data.keys())[0]] = data[list(data.keys())[0]]
    xs = list(radar_vals.keys())
    ys = list(radar_vals.values())

    ax.clear()
    ax.scatter(xs, ys)
    plt.xticks(rotation=45, ha='right')
    plt.xlim([0, 180])
    plt.ylim([0, 1.5])
    plt.subplots_adjust(bottom=0.30)
    plt.title('RADAR values')
    plt.ylabel('Distance')
    plt.xlabel('Angle')


# Set up plot to call animate() function periodically
ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
