# To use this library with a sensor connected to your Raspberry Pi or other I2C-enabled device,
# you would create an instance of the SpectralSensor class with the appropriate bus number and
# sensor address. Then you could call its read_channel or read_spectrum methods to get the latest
# spectral data from the sensor. For example:

# sensor = SpectralSensor(address=0x64)
# channel_0_value = sensor.read_channel(0)
# spectral_values = sensor.read_spectrum()

# This would read the spectral value for channel 0 of the sensor and store it in the 'channel_0_value'
# variable, as well as reading all 64 spectral values into the 'spectral_values' list. Note that you
# would need to modify this code to match the specific requirements of your sensor, including the
# I2C address and register addresses for reading channel data.

import smbus

class SpectralSensor:
    def __init__(self, bus=1, address=0x64):
        self.bus = smbus.SMBus(bus)
        self.address = address

        # Configure sensor for continuous measurement mode
        self.bus.write_byte_data(self.address, 0x00, 0x00)

    def read_channel(self, channel):
        # Read raw data for the specified channel
        reg = 0x09 + channel * 2
        data = self.bus.read_i2c_block_data(self.address, reg, 2)

        # Convert raw data to spectral value
        spectral_value = (data[0] << 8) | data[1]

        return spectral_value

    def read_spectrum(self):
        # Read raw spectral data from sensor
        data = self.bus.read_i2c_block_data(self.address, 0x09, 128)

        # Convert raw data to spectral values
        spectral_values = []
        for i in range(0, 128, 2):
            raw_value = data[i] << 8 | data[i+1]
            spectral_values.append(raw_value)

        return spectral_values
