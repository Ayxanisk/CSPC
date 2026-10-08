import numpy as np
import matplotlib.pyplot as plt

t, x, y = np.loadtxt("trajectory.csv", delimiter=",", skiprows=1, unpack=True)

v_x = np.gradient(x, t)
v_y = np.gradient(y, t)
speed = np.sqrt(v_x**2 + v_y**2)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(x, y, 'b.-', label='Trajectory')
ax1.set_xlabel('X position')
ax1.set_ylabel('Y position')
ax1.set_title('2D Tracked Path (X vs Y)')
ax1.grid(True)
ax1.legend()

ax2.plot(t, speed, 'r-', label=r'Speed $\sqrt{v_x^2 + v_y^2}$')
ax2.set_xlabel('Time (s)')
ax2.set_ylabel('Speed (m/s)')
ax2.set_title('Speed over Time')
ax2.grid(True)
ax2.legend()

plt.savefig('trajectory.png')