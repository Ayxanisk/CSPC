"""
PW2 Lab B Part 5 (bonus) -- find a titration's equivalence point.

titration.csv holds a titration curve: pH versus the volume of base added.
The equivalence point is the volume where the pH changes fastest (the steep
jump). Numerically, that is where the SLOPE of the pH curve is largest.
Run:  python titration.py
"""
import numpy as np
import matplotlib.pyplot as plt

# TODO 1: read titration.csv (columns volume_base, pH) into arrays V, pH.
data = np.genfromtxt("titration.csv", delimiter=",", names=True)
V = data["volume_base"]
pH = data["pH"]

# TODO 2: compute the slope of the pH curve with np.gradient(pH, V), and find
#         the volume where that slope is largest (np.argmax). That is the
#         equivalence point. Print it.
slope = np.gradient(pH, V)
max_idx = np.argmax(slope)
v_eq = V[max_idx]
max_slope = slope[max_idx]

print(f"Equivalence point volume: {v_eq:.2f} mL (max slope = {max_slope:.4f} pH/mL)")

# TODO 3: make two plots side by side: (left) pH vs volume with a line at the
#         equivalence point; (right) the slope vs volume, showing it peaks
#         at the equivalence point. Save as titration.png.
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left plot: Titration curve
ax1.plot(V, pH, "b.-", label="pH curve", linewidth=1.5)
ax1.axvline(v_eq, color="red", linestyle="--", label=f"Equiv. pt ({v_eq:.2f} mL)")
ax1.set_xlabel("Volume of Base Added (mL)")
ax1.set_ylabel("pH")
ax1.set_title("Titration Curve")
ax1.grid(True, linestyle=":", alpha=0.6)
ax1.legend()

# Right plot: Slope (first derivative)
ax2.plot(V, slope, "g.-", label=r"$\frac{dpH}{dV}$", linewidth=1.5)
ax2.axvline(v_eq, color="red", linestyle="--", label=f"Peak ({v_eq:.2f} mL)")
ax2.plot(v_eq, max_slope, "ro")
ax2.set_xlabel("Volume of Base Added (mL)")
ax2.set_ylabel(r"Slope $\left(\frac{dpH}{dV}\right)$")
ax2.set_title("First Derivative (Slope) Curve")
ax2.grid(True, linestyle=":", alpha=0.6)
ax2.legend()

plt.tight_layout()
plt.savefig("titration.png", dpi=300)
plt.close()