# Suitcase Spectroscopy Version 1.1
# Thomas M. Van Pelt 2023

# The script defines several functions for displaying weather data, saving graphs of sensor readings,
# displaying a QR code, and powering down the Raspberry Pi. The main loop of the script continuously
# checks for button presses on the Inky Impression and calls the appropriate function based on the
# button pressed. The connect_to_wifi function connects the Raspberry Pi to a specified Wi-Fi network
# using the provided SSID and password. The display_weather function queries a weather API to get the
# closest weather data based on the Raspberry Pi's IP address, creates an image with the weather data,
# and displays the image on the Inky Impression display. The save_graph function creates an image with
# a line graph of the current sensor readings for all visible channels, and saves the image to the
# specified image directory. The display_qr function opens an image file with a QR code containing
# information about the Raspberry Pi's owner, and displays the image on the Inky Impression display.
# The power_down function displays the QR code image, and then powers down the Raspberry Pi. Overall,
# this script provides a simple interface for displaying weather data, saving sensor data, displaying
# a QR code, and powering down the Raspberry Pi using the Inky Impression display and buttons.

import os
import time
from inky import InkyImpression
from PIL import Image, ImageDraw
from ams.as7341 import AS7341
import network
import numpy as np
import matplotlib.pyplot as plt


# Define the SSID and password of your WiFi network
WIFI_SSID = 'your_wifi_ssid'
WIFI_PASSWORD = 'your_wifi_password'


# Define the path to the image directory on the Raspberry Pi's desktop
image_dir = "/home/pi/Desktop/image"


# Initialize the Inky Impression display
inky_display = InkyImpression("red", (800, 480))
inky_display.set_border(inky_display.WHITE)


# Initialize the AS7341 sensor
as7341 = AS7341()


# Connect to your local WiFi network
def connect_to_wifi(ssid, password):
    station = network.WLAN(network.STA_IF)
    if not station.isconnected():
        print('Connecting to WiFi...')
        station.active(True)
        station.connect(ssid, password)
        while not station.isconnected():
            time.sleep(1)
    print('WiFi Connection successful')
    print(station.ifconfig())
    return station.ifconfig()[0]


# Invoke connect_to_wifi function to connect to WiFi network
connect_to_wifi(WIFI_SSID, WIFI_PASSWORD)


def get_weather_conditions():
    try:
        # Request weather data from OpenWeatherMap API
        response = requests.get(f"http://api.openweathermap.org/data/2.5/weather?q={CITY}&appid={API_KEY}&units=metric")
        data = response.json()

        # Extract relevant weather data
        temperature = round(data["main"]["temp"])
        feels_like = round(data["main"]["feels_like"])
        description = data["weather"][0]["description"].capitalize()
        humidity = data["main"]["humidity"]
        wind_speed = data["wind"]["speed"]

        # Construct weather conditions string
        conditions = f"{description}, {temperature}°C (Feels like {feels_like}°C)\nHumidity: {humidity}%\nWind speed: {wind_speed} m/s"
    except:
        # If an error occurs, return an error message
        conditions = "Unable to retrieve weather conditions"
    
    return conditions


def get_spectrum_readings():
    # Initialize the AS7341 sensor
    sensor = AS7341()

    # Set the integration time and gain
    sensor.integration_time = 500
    sensor.gain = 1

    # Set the channel control to read the visible spectrum (channels 0-5)
    sensor.channel_control = 0b0000000011111111

    # Take readings from the sensor
    readings = []
    for i in range(6):
        readings.append(sensor.channel_data[i])

    return readings

def display_spectrum_graph(readings):
    # Initialize the Inky Impression display.
    inky_display = InkyImpression('red')
    image = Image.new('P', (inky_display.WIDTH, inky_display.HEIGHT))
    draw = ImageDraw.Draw(image)
    
    # Draw the line graph.
    x_scale = inky_display.WIDTH / len(readings)
    y_scale = inky_display.HEIGHT / 65535
    for i in range(len(readings) - 1):
        x1 = i * x_scale
        y1 = inky_display.HEIGHT - (readings[i] * y_scale)
        x2 = (i + 1) * x_scale
        y2 = inky_display.HEIGHT - (readings[i + 1] * y_scale)
        draw.line((x1, y1, x2, y2), fill=inky_display.BLACK)
    
    # Add a label to the graph.
    label = 'Suitcase Spectroscopy 1.01'
    label_width, label_height = draw.textsize(label)
    label_x = (inky_display.WIDTH - label_width) / 2
    label_y = inky_display.HEIGHT - label_height - 5
    draw.text((label_x, label_y), label, fill=inky_display.BLACK)
    
    # Display the graph on the Inky Impression.
    inky_display.set_image(image)
    inky_display.show()


def display_weather(inky_display):
    # Display current weather conditions on the Inky Impression
    # ...
    # ...
    inky_display.set_image(Image.open("/home/pi/Desktop/images/weather.png"))
    inky_display.show()
    
    
def display_spectroscopy():
    # Read current readings from the as7341 sensor for the visible spectrum
    visible_spectrum = as7341.read_visible_spectrum()

    # Generate a line graph of the visible spectrum readings using Matplotlib
    plt.plot(np.arange(len(visible_spectrum)), visible_spectrum)
    plt.title("Suitcase Spectroscopy 1.01")
    plt.xlabel("Wavelength (nm)")
    plt.ylabel("Intensity")
    plt.savefig("/home/pi/Desktop/images/spectroscopy.png")
    plt.clf()


def handle_button_press(button, inky_display):
    if button == "a":
        display_weather(inky_display)
    elif button == "b":
        display_spectroscopy()
        inky_display.set_image(Image.open("/home/pi/Desktop/images/spectroscopy.png"))
        inky_display.show()
    elif button == "c":
        inky_display.set_image(Image.open("/home/pi/Desktop/images/owner-qr.png"))
        inky_display.show()
    elif button == "d":
        inky_display.set_image(Image.open("/home/pi/Desktop/images/owner-qr.png"))
        inky_display.show()
        time.sleep(5)
        inky_display.set_image(Image.open("/home/pi/Desktop/images/goodbye.png"))
        inky_display.show()
        os.system("sudo poweroff")


while True:
    # check if button 'a' is pressed
    if button_a.is_pressed:
        # get current weather conditions
        weather_conditions = get_weather_conditions()
        # display weather conditions on Inky Impression
        inky_display.set_image(weather_conditions)
        inky_display.show()
        
    # check if button 'b' is pressed
    if button_b.is_pressed:
        # take current readings only in the visible spectrum from the as7341 sensor
        visible_spectrum_readings = get_visible_spectrum_readings()
        # display a line graph of those results labeled as Suitcase Spectroscopy 1.01 on the Inky Impression 7.3" HAT
        inky_display.set_image(create_line_graph(visible_spectrum_readings, label="Suitcase Spectroscopy 1.01"))
        inky_display.show()
    
    # check if button 'c' is pressed
    if button_c.is_pressed:
        # display owner-qr.png which is stored in the images folder on the desktop on the inky impression
        inky_display.set_image(Image.open('/home/pi/Desktop/inky-impression/images/owner-qr.png'))
        inky_display.show()

    # check if button 'd' is pressed
    if button_d.is_pressed:
        # display owner-qr.png which is stored in the images folder on the desktop on the inky impression
        inky_display.set_image(Image.open('/home/pi/Desktop/inky-impression/images/owner-qr.png'))
        inky_display.show()
        # power down all devices including the raspberry pi 4
        subprocess.call(['sudo', 'shutdown', '-h', 'now'])

    # wait for 0.1 seconds to prevent CPU hogging
    time.sleep(0.1)