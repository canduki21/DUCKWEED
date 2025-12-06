from machine import I2C
import time

ADDR = 0x39

# Registers
ENABLE = 0x80
ATIME = 0x81
ASTEP_L = 0xCA
ASTEP_H = 0xCB
CONTROL = 0xAF
STATUS = 0xA3
CH_DATA = 0x95   # Start of data registers

class AS7343:
    def __init__(self, i2c):
        self.i2c = i2c
        # Power on
        self._write(ENABLE, 0x01)
        time.sleep(0.01)
        # Enable spectral measurement engine
        self._write(ENABLE, 0x05)

        # Integration settings
        self._write(ATIME, 100)
        self._write(ASTEP_L, 0xFF)
        self._write(ASTEP_H, 0x03)

        print("AS7343 initialized.")

    def _write(self, reg, val):
        self.i2c.writeto_mem(ADDR, reg, bytes([val]))

    def _read(self, reg, length):
        return self.i2c.readfrom_mem(ADDR, reg, length)

    def read_channels(self):
        # Trigger measurement
        self._write(CONTROL, 0x01)

        # Wait for STATUS ready with timeout
        timeout = time.ticks_ms() + 200
        while time.ticks_ms() < timeout:
            status = self._read(STATUS, 1)[0]
            if status & 0x08:
                break

        # Read all 12 channels (24 bytes)
        raw = self._read(CH_DATA, 24)
        channels = []

        for i in range(0, 24, 2):
            low = raw[i]
            high = raw[i + 1]
            channels.append(high << 8 | low)

        return channels
