###
#AS7341 Sensor          Raspberry Pi Pico
#-----------          -------------------
#VCC (3.3V) ---------- 3V3
#GND ------------------ GND
#SDA ------------------ GP26 (SDA)
#SCL ------------------ GP27 (SCL)
#
#Waveshare 5.65 inch e-Paper Display
#------------------- -------------------
#VCC (3.3V) ---------- 3V3
#GND ------------------ GND
#CLK ------------------ GP25 (SCK)
#MOSI ---------------- GP24 (MOSI)
#MISO ---------------- GP23 (MISO)
#CS ------------------- GP22 (D5)
#DC ------------------- GP21 (D6)
#RST ------------------ GP20 (D4)
#BUSY ---------------- GP19 (D3)
###

import time
import asyncio
import busio
import board
from as7341 import AS7341
from waveshare_epd import epd5in65
import cp_pillow as pillow

# Initialize the I2C bus for communication with the AS7341 sensor
i2c = busio.I2C(board.GP27, board.GP26)

# Initialize the AS7341 sensor
as7341 = AS7341(i2c)

# Initialize the Waveshare 5.65 inch e-Paper Display
spi = busio.SPI(board.GP25, MOSI=board.GP24, MISO=board.GP23)
epd = epd5in65.EPD(spi, cs_pin=board.GP22, dc_pin=board.GP21, rst_pin=board.GP20, busy_pin=board.GP19)
epd.init()

# Initialize variables to store the spectral readings
spectral_readings = []

def display_spectral_data(spectral_data):
    # Create the image buffer for the e-Paper Display
    image = Image.new('1', (epd.width, epd.height), 255)
    draw = ImageDraw.Draw(image)

    # Plot the spectral data as a line graph
    for i in range(len(spectral_data) - 1):
        x0 = int(i / len(spectral_data) * epd.width)
        y0 = int(spectral_data[i] / 4096 * epd.height)
        x1 = int((i + 1) / len(spectral_data) * epd.width)
        y1 = int(spectral_data[i + 1] / 4096 * epd.height)
        draw.line((x0, y0, x1, y1), fill = 0)

    # Display the image buffer on the e-Paper Display
    epd.display_frame(epd.get_frame_buffer(image))

async def update_spectral_data():
    while True:
        # Read the spectral data from the AS7341 sensor
        spectral_data = as7341.get_spectral_data()

        # Add the spectral data to the list of readings
        spectral_readings.append(spectral_data)

        # Display the latest spectral data on the e-Paper Display
        display_spectral_data(spectral_data)

        # Sleep for a short period of time before checking again
        await asyncio.sleep(0.1)

# Start the asyncio loop to continuously update the spectral data
loop = asyncio.get_event_loop()
loop.run_until_complete(update_spectral_data())
loop.close()
