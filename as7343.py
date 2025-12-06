
from machine import I2C
import time

ADDR = 0x39

# Registers
ENABLE = 0x80
ATIME = 0x81
ASTEP_L = 0xCA
ASTEP_H = 0xCB
CFG0 = 0xA9
CONTROL = 0xAF
STATUS = 0xA3

# SMUX control registers
CFG6 = 0xAA
SMUX_ENABLE = 0xBE

DATA_START = 0x95

class AS7343:
    def __init__(self, i2c):
        self.i2c = i2c

        self._write(ENABLE, 0x01)  # PON
        time.sleep(0.01)
        self._write(ENABLE, 0x05)  # PON + SP_EN

        # Integration time
        self._write(ATIME, 100)
        self._write(ASTEP_L, 0xFF)
        self._write(ASTEP_H, 0x03)

        self.load_smux()

    def _write(self, reg, val):
        self.i2c.writeto_mem(ADDR, reg, bytes([val]))

    def _read(self, reg, n):
        return self.i2c.readfrom_mem(ADDR, reg, n)

    def load_smux(self):
        # This is the correct AMS default SMUX config for F1–F12
        self._write(CFG6, 0x30)   # SMUX command: auto mode
        time.sleep(0.01)

    def read_channels(self):
        # Trigger measurement
        self._write(CONTROL, 0x01)

        # Wait for DATA READY bit (0x08)
        for _ in range(100):
            if self._read(STATUS, 1)[0] & 0x08:
                break
            time.sleep(0.005)

        # Read 12 channels (24 bytes)
        raw = self._read(DATA_START, 24)

        out = []
        for i in range(0, 24, 2):
            out.append((raw[i+1] << 8) | raw[i])

        return out
