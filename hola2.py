from machine import I2C, Pin

i2c = I2C(1, scl=Pin(14), sda=Pin(13))

try:
    v = i2c.readfrom_mem(0x39, 0x80, 1)
    print("ENABLE:", v)
except Exception as e:
    print("ERR:", e)
