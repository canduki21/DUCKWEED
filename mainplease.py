from machine import I2C, Pin
import time
from as7343 import AS7343

# Your pins: SCL=GP14, SDA=GP13
i2c = I2C(1, scl=Pin(14), sda=Pin(13), freq=400000)

sensor = AS7343(i2c)

print("Device connected:", sensor.begin())

sensor.power_on()
sensor.set_integration()
sensor.enable_spectral()

time.sleep(0.1)

while True:
    ch = sensor.read_all_channels()
    print("CH:", ch)
    time.sleep(0.5)
