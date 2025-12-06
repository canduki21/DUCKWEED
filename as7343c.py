from machine import I2C
import time

ADDR = 0x39

# Register addresses
ENABLE = 0x80
ATIME = 0x81
ASTEP_L = 0xCA
ASTEP_H = 0xCB
CONTROL = 0xAF
STATUS = 0xA3
DATA_START = 0x95

class AS7343:
    def __init__(self, i2c):
        self.i2c = i2c

        # Power ON
        self._w(ENABLE, 0x01)
        time.sleep(0.02)

        # Enable spectral measurement
        self._w(ENABLE, 0x05)

        # Integration settings
        self._w(ATIME, 100)
        self._w(ASTEP_L, 0xFF)
        self._w(ASTEP_H, 0x03)

        # Load SparkFun SMUX mode for AS7343C
        self.load_smux()

    def _w(self, reg, val):
        self.i2c.writeto_mem(ADDR, reg, bytes([val]))

    def _r(self, reg, n=1):
        return self.i2c.readfrom_mem(ADDR, reg, n)

    def load_smux(self):
        # SparkFun AS7343C auto-SMUX load
        self._w(0xBE, 0x30)   # Internal auto SMUX mode
        time.sleep(0.02)

    def read_channels(self):
        # Start measurement
        self._w(CONTROL, 0x01)
        time.sleep(0.05)

        # Read 12 channels (24 bytes)
        raw = self._r(DATA_START, 24)
        out = []

        for i in range(0, 24, 2):
            out.append(raw[i+1] << 8 | raw[i])

        return out
