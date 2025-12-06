from machine import I2C, Pin

i2c = I2C(1, scl=Pin(19), sda=Pin(18))

status = i2c.readfrom_mem(0x39, 0xA3, 1)[0]
print("STATUS =", hex(status))
