from machine import I2C
import time

AS7343_ADDR = 0x39

# Register definitions
ENABLE = 0x80
ATIME = 0x81
ASTEP_L = 0xCA
ASTEP_H = 0xCB
CFG0 = 0xA9
CONTROL = 0xAF
STATUS = 0xA3
CH_DATA_START = 0x95

class AS7343:
    def __init__(self, i2c, address=AS7343_ADDR):
        self.i2c = i2c
        self.address = address
        # Power ON
        self._write(ENABLE, 0x01)
        time.sleep(0.01)
        # PON + Spectral Measurement Enable
        self._write(ENABLE, 0x05)
        # Default config
        self._configure()

    def _write(self, reg, val):
        self.i2c.writeto_mem(self.address, reg, bytes([val]))

    def _read(self, reg, n):
        return self.i2c.readfrom_mem(self.address, reg, n)

    def _read_word(self, reg):
        data = self._read(reg, 2)
        return data[1] << 8 | data[0]

    def _configure(self):
        # Integration time = (ATIME+1)*(ASTEP+1)*2.78us
        self._write(ATIME, 100)
        self._write(ASTEP_L, 0xFF)
        self._write(ASTEP_H, 0x03)
        # Set measurement mode (F1–F4 mapping first)
        self._write(CFG0, 0x10)
        # Start measurement
        self._write(CONTROL, 0x01)

    def ready(self):
        status = self._read(STATUS, 1)[0]
        return bool(status & 0x08)

    def read_channels(self):
        # Wait until data is ready
        while not self.ready():
            time.sleep(0.005)

        # AS7343 returns 12 channels (F1–F12)
        channels = []
        for reg in range(CH_DATA_START, CH_DATA_START + 24, 2):
            channels.append(self._read_word(reg))

        return channels
