# This code is for an electronic project that uses the Adafruit AS7262 Visible Light Sensor, an I2C interface,
# an ePaper display, and a tactile switch. The code starts by importing the necessary libraries for the project,
# including busio for I2C communication, digitalio for the switch, adafruit_as7262 for the light sensor,
# displayio and terminalio for the display, and numpy and matplotlib for numerical calculations and plotting.
# Next, the code creates an I2C object to communicate with the sensor and initializes the sensor. It also
# initializes the display and creates a switch object. The code then defines the number of readings to store
# (num_readings) and the arrays to store the readings (x and y). It then creates a line graph using matplotlib
# with appropriate labels and limits, and saves the graph as a PNG file. The code then enters an infinite loop
# that waits for the switch to be pressed. When the switch is pressed, it reads the visible light intensity from
# the sensor, adds the reading to the y array, updates the line graph, redraws the display, and waits for the
# switch to be released.

import busio
import digitalio
import adafruit_as7262
import time
import displayio
import terminalio
import numpy as np
import matplotlib.pyplot as plt

# create the i2c object for the Pico
i2c = busio.I2C(board.GP1, board.GP0)

# initialize the AS7262 sensor
sensor = adafruit_as7262.AS7262(i2c)

# initialize the display
display = board.DISPLAY
group = displayio.Group(max_size=10)
display.show(group)

# create the tactile switch object
switch = digitalio.DigitalInOut(board.D5)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

# define the number of readings to store
num_readings = 50

# define the arrays to store the readings
x = np.arange(0, num_readings)
y = np.zeros(num_readings)

# create the line graph
fig, ax = plt.subplots()
line, = ax.plot(x, y)

# add labels and limits to the graph
ax.set_xlabel("Reading Number")
ax.set_ylabel("Visible Spectrum Intensity")
ax.set_ylim(0, 100)

# save the graph as a png
plt.savefig("line_graph.png")

# display the graph on the epaper display
with open("line_graph.png", "rb") as f:
    image = displayio.OnDiskBitmap(f)
    image_sprite = displayio.TileGrid(image, pixel_shader=displayio.ColorConverter(), x=0, y=0)
    group.append(image_sprite)

while True:
    # wait until the switch is pressed
    while switch.value:
        pass

    # read the AS7262 data
    sensor.convert_spectral_data()
    v_int = sensor.get_visible()

    # add the reading to the array
    y[:-1] = y[1:]
    y[-1] = v_int

    # update the line graph
    line.set_ydata(y)

    # redraw the display
    display.refresh(target_frames_per_second=60)

    # wait until the switch is released
    while not switch.value:
        pass
