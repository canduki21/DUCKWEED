from machine import I2C, Pin
import time

AS7343_ADDR = 0x39

# Register map (minimal subset)
ENABLE      = 0x80
ATIME       = 0x81
ASTEP_L     = 0xCA
ASTEP_H     = 0xCB
CFG0        = 0xA9
CONTROL     = 0x8F
STATUS      = 0x93

DATA_START  = 0x95   # First channel (2 bytes each)

class AS7343:
    def __init__(self, i2c):
        self.i2c = i2c

    def _w(self, reg, val):
        self.i2c.writeto_mem(AS7343_ADDR, reg, bytes([val]))

    def _r(self, reg):
        return self.i2c.readfrom_mem(AS7343_ADDR, reg, 1)[0]

    def _r16(self, reg):
        d = self.i2c.readfrom_mem(AS7343_ADDR, reg, 2)
        return d[1] << 8 | d[0]

    def begin(self):
        try:
            device_id = self._r(0x92)
            return device_id == 0x24
        except:
            return False

    def power_on(self):
        self._w(ENABLE, 0x01)
        time.sleep(0.01)

    def enable_spectral(self):
        self._w(ENABLE, 0x05)   # PON + SP_EN
        time.sleep(0.01)

    def set_integration(self, atime=0xFF, astep=0x0080):
        self._w(ATIME, atime)
        self._w(ASTEP_L, astep & 0xFF)
        self._w(ASTEP_H, astep >> 8)

    def read_all_channels(self):
        """Reads 6 main channels (not full 18 yet)."""
        ch = []
        for off in range(0, 12, 2):
            ch.append(self._r16(DATA_START + off))
        return ch

