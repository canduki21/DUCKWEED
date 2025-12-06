from machine import I2C, Pin
import time

AS7343_ADDR = 0x39

# Registers
ENABLE = 0x80
ATIME  = 0x81
ASTEP_L = 0xCA
ASTEP_H = 0xCB
CFG0 = 0xA9
CONTROL = 0x8F
STATUS = 0x93

# Data registers (spectral channels)
DATA_START = 0x95  # 12 bytes, 6 channels (low + high)

i2c = I2C(1, scl=Pin(15), sda=Pin(14), freq=400000)

def write_reg(reg, val):
    i2c.writeto_mem(AS7343_ADDR, reg, bytes([val]))

def read_reg(reg):
    return i2c.readfrom_mem(AS7343_ADDR, reg, 1)[0]

def read_2(reg):
    b = i2c.readfrom_mem(AS7343_ADDR, reg, 2)
    return b[1] << 8 | b[0]

# --- Initialization sequence ---
print("ID before init:", read_reg(0x92))

write_reg(ENABLE, 0x01)   # Power ON
time.sleep(0.02)

write_reg(ATIME, 0xFF)    # Integration time low = long exposure
write_reg(ASTEP_L, 0x80)
write_reg(ASTEP_H, 0x00)

write_reg(CFG0, 0x00)     # Measurement mode 0
write_reg(CONTROL, 0x01)  # Enable SMUX
time.sleep(0.02)

write_reg(ENABLE, 0x05)   # PON + SP_EN
time.sleep(0.05)

while True:
    status = read_reg(STATUS)
    print("Status:", hex(status))

    # Read channels
    ch = []
    for offset in range(0, 12, 2):
        ch.append(read_2(DATA_START + offset))

    print("Channels:", ch)
    time.sleep(1)
