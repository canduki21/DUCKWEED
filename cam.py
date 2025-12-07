import os
os.environ["BLINKA_MLX90640_FORCE_BLOCK"] = "16"

import time
import numpy as np
import matplotlib.pyplot as plt
import board
import busio
import adafruit_mlx90640

# Initialize I2C
i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)

# Initialize sensor
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_1_HZ

frame = [0] * 768  # 32 x 24

# Plot setup
plt.ion()
fig, ax = plt.subplots(figsize=(6,4))

thermal_img = ax.imshow(
    np.zeros((24, 32)),
    cmap='inferno',
    vmin=20,  # lower temperature threshold
    vmax=40   # upper temperature threshold
)

plt.colorbar(thermal_img)
plt.title("MLX90640 Thermal Camera")

while True:
    try:
        mlx.getFrame(frame)
        data = np.reshape(frame, (24, 32))

        thermal_img.set_data(data)
        plt.draw()
        plt.pause(0.01)

    except Exception as e:
        print("Frame error:", e)
