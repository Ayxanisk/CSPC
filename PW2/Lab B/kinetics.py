"""
PW2 Lab B Part 3 -- fit a reaction's rate constant to measured data.

A first-order reaction decays as  C(t) = C0 * exp(-k*t).  You have noisy
concentration-vs-time measurements; find the k that best matches them.
Complete the TODOs. Run:  python kinetics.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import minimize

# TODO 1: 
# read kinetics.csv (columns time, concentration) into arrays t, C.
#         Set C0 = the first concentration.
time, concentration = np.loadtxt("kinetics.csv", delimiter=",",skiprows=1,unpack=True)

C0 = concentration[0]

# TODO 2: write total_error(k) = sum of (measured - C0*exp(-k*t))^2.
#         This is the "how bad" number: small when the model matches the data.
def total_error(k):
    return np.sum((concentration - C0 * np.exp(-k * time)) ** 2)

# TODO 3: minimise total_error wii th scipy.optimize.minimize (method "SLSQP",
#         bounds [(0, 5)], start x0=0.5). Print the fitted k.
result = minimize(total_error,x0=[0.5],method="SLSQP",bounds=[(0,5)])
k_fitted = result.x[0]
print(f"Fitted :{k_fitted}")    

# TODO 4: plot the measured data (points) and your fitted curve (line) together.
#         Save as kinetics.png.

plt.figure(figsize=(8, 5))
plt.scatter(time, concentration, label="Measured Data", color="blue", zorder=5)

t_smooth = np.linspace(time.min(), time.max(), 200)
C_smooth = C0 * np.exp(-k_fitted * t_smooth)
plt.plot(t_smooth, C_smooth, label=f"Fitted Curve (k = {k_fitted:.4f})", color="red", linewidth=2)

plt.xlabel("Time")
plt.ylabel("Concentration")
plt.legend()
plt.grid(True, linestyle="--", alpha=0.6)
plt.savefig("kinetics.png", dpi=300, bbox_inches="tight")
