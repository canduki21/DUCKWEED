from machine import Pin, I2C
import time
from as7343 import AS7343

# GP18 = SDA, GP19 = SCL on Pico
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)

print("I2C scan:", i2c.scan())

sensor = AS7343(i2c)

while True:
    data = sensor.read_channels()
    print("Spectral Channels:", data)
    time.sleep(1)
