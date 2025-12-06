from machine import Pin, I2C
import time
from as7343 import AS7343

i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)

print("I2C scan:", i2c.scan())

sensor = AS7343(i2c)

while True:
    vals = sensor.read_channels()
    print(vals)
    time.sleep(1)
