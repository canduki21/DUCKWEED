from machine import I2C
import time

ADDR = 0x39

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

        # Power on + spectral engine enable
        self._w(ENABLE, 0x01)
        time.sleep(0.01)
        self._w(ENABLE, 0x05)

        # Integration time
        self._w(ATIME, 100)
        self._w(ASTEP_L, 0xFF)
        self._w(ASTEP_H, 0x03)

        # Load *AS7343C-specific* SMUX
        self.load_smux_c()

    def _w(self, reg, val):
        self.i2c.writeto_mem(ADDR, reg, bytes([val]))

    def _r(self, reg, n=1):
        return self.i2c.readfrom_mem(ADDR, reg, n)

    def load_smux_c(self):
        # This is the correct auto-SMUX mode for AS7343C
        # It activates all 12 channels (SparkFun mapping)
        self._w(0xBE, 0x70)
        time.sleep(0.02)

    def read_channels(self):
        # Start measurement
        self._w(CONTROL, 0x01)
        time.sleep(0.05)

        # Read 24 bytes (12 channels)
        raw = self._r(DATA_START, 24)
        ch = []

        for i in range(0, 24, 2):
            ch.append((raw[i+1] << 8) | raw[i])

        return ch
