from machine import I2C, Pin

i2c = I2C(1, scl=Pin(19), sda=Pin(18))

def r(reg):
    return hex(i2c.readfrom_mem(0x39, reg, 1)[0])

print("ENABLE =", r(0x80))
print("CFG0   =", r(0xA9))
print("CONTROL=", r(0xAF))
print("STATUS =", r(0xA3))
