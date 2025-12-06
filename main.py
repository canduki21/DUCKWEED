from machine import Pin, I2C
import time
from as7343 import AS7343

# I2C1 pins: SDA = GP18 (pin 24), SCL = GP19 (pin 25)
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)

print("I2C scan:", i2c.scan())

sensor = AS7343(i2c)
print("Sensor initialized.")

while True:
    data = sensor.read_channels()
    print("Spectral channels:", data)
    time.sleep(1)
