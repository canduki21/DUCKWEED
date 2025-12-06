from machine import Pin, I2C
import time
from as7343 import AS7343

# I2C1 pins: SDA = GP18, SCL = GP19
i2c = I2C(1, scl=Pin(19), sda=Pin(18), freq=400000)

print("Scanning I2C bus...")
time.sleep(1)
devices = i2c.scan()
print("Found I2C devices:", devices)

if 0x39 not in devices:
    print("ERROR: AS7343 NOT detected! Check wiring (SDA=GP18, SCL=GP19).")
else:
    print("AS7343 detected successfully at address 0x39!")

sensor = AS7343(i2c)

while True:
    data = sensor.read_channels()
    print("Spectral channels:", data)
    time.sleep(1)
