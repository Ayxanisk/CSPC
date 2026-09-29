"""
PW2 Lab A -- Motion from tracking data.

Read noisy free-fall position measurements, then:
  - differentiate once  -> velocity
  - differentiate twice -> acceleration (should be ~ constant -g, but noisy!)
  - integrate the acceleration back up -> recover velocity and position

Complete the TODOs. Run:  python analysis.py
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import cumulative_trapezoid

# TODO 1: read freefall.csv into arrays t and y
#         (hint: np.loadtxt with a comma delimiter, skipping the header)
t, y = np.loadtxt("freefall.csv", delimiter=",",skiprows=1,unpack=True)




# TODO 2: compute velocity v = derivative of y w.r.t. t   (np.gradient)
#         and acceleration a = derivative of v w.r.t. t    (np.gradient again)
#         Print the mean acceleration. Is it close to -9.81? Is it noisy?

v = np.gradient(y,t)
a = np.gradient(v,t)

mean_a = np.mean(a)

print("mean a = ",mean_a)

# TODO 3: integrate a back up to recover velocity and position
#         (hint: cumulative_trapezoid(a, t, initial=0) + v[0], then again)

v_recovery = cumulative_trapezoid(a, t, initial=0) + v[0]
y_recovery = cumulative_trapezoid(v_recovery, t, initial=0) + y[0]

std = np.std(a)
print(std)

print("error", np.abs(y_recovery - y).max())
# TODO 4: make a figure with 3 stacked panels: position, velocity, acceleration
#         vs time. Mark the true -9.81 line on the acceleration panel.
#         Save it as motion.png

fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(8, 10), sharex=True)

ax1.plot(t, y, 'b.', label='Measured')
ax1.plot(t, y_recovery, 'r--', label='Reconstructed')
ax1.set_ylabel('Position (m)')
ax1.set_title('Free Fall Analysis')
ax1.legend()
ax1.grid(True)

ax2.plot(t, v, 'g-', label='Computed (gradient)')
ax2.plot(t, v_recovery, 'm--', label='Reconstructed')
ax2.set_ylabel('Velocity (m/s)')
ax2.legend()
ax2.grid(True)


ax3.plot(t, a, 'c-', label='Computed acceleration')
ax3.axhline(-9.81, color='r', linestyle='--', label='True g (-9.81 m/s²)')
ax3.set_xlabel('Time (s)')
ax3.set_ylabel('Acceleration (m/s²)')
ax3.legend()
ax3.grid(True)

plt.savefig('motion.png')