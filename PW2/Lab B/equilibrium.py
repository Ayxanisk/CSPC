"""
PW2 Lab B Part 4 -- chemical equilibrium via the equilibrium constant K.

Reaction  H2 + I2 <=> 2 HI, starting from 1 mol H2 and 1 mol I2.
As the reaction proceeds by an extent x:  H2 = 1-x,  I2 = 1-x,  HI = 2x.
At equilibrium the composition satisfies the equilibrium constant
        K = [HI]^2 / ([H2][I2]) = (2x)^2 / ((1-x)(1-x)).
Given K, find the extent x. Solve it TWO ways and compare.
Run:  python equilibrium.py
"""
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import newton, minimize

K = 15.6
a = b = 1.0

# TODO 1: write k_imbalance(x) = (2x)^2/((a-x)(b-x)) - K.
#         It equals zero exactly at equilibrium.
def k_imbalance(x):
    return ((2 * x) ** 2) / ((a - x) * (b - x)) - K

# TODO 2 (method 1): use scipy.optimize.newton to find the root of k_imbalance
#         (start x0=0.5). This is root-finding.
x_newton = newton(k_imbalance, x0=0.5)

# TODO 3 (method 2): use scipy.optimize.minimize to minimise k_imbalance(x)**2
#         (method "SLSQP", bounds [(0, 0.999)], x0=[0.5]). Print both answers
#         and confirm they agree.
def objective(x):
    return k_imbalance(x[0]) ** 2

res_slsqp = minimize(objective, x0=[0.5], method="SLSQP", bounds=[(0, 0.999)])
x_slsqp = res_slsqp.x[0]

print(f"Method 1 (Newton root-finding): x = {x_newton:.6f}")
print(f"Method 2 (SLSQP minimization):  x = {x_slsqp:.6f}")
print(f"Difference: {abs(x_newton - x_slsqp):.2e}")

# TODO 4: report the equilibrium amounts (H2, I2, HI), and plot how the three
#         amounts change with the extent x, marking the equilibrium. Save
#         equilibrium.png.
x_eq = x_newton
h2_eq = a - x_eq
i2_eq = b - x_eq
hi_eq = 2 * x_eq

print("\n--- Equilibrium Composition ---")
print(f"H2: {h2_eq:.4f} mol")
print(f"I2: {i2_eq:.4f} mol")
print(f"HI: {hi_eq:.4f} mol")

x_vals = np.linspace(0, 0.99, 500)
h2_vals = a - x_vals
i2_vals = b - x_vals
hi_vals = 2 * x_vals

plt.figure(figsize=(8, 5))
plt.plot(x_vals, h2_vals, label="H2 / I2", color="blue", linewidth=2)
plt.plot(x_vals, hi_vals, label="HI", color="green", linewidth=2)
plt.axvline(x=x_eq, color="red", linestyle="--", label=f"Equilibrium (x = {x_eq:.4f})")
plt.scatter([x_eq, x_eq], [h2_eq, hi_eq], color="red", zorder=5)

plt.xlabel("Extent of Reaction x (mol)")
plt.ylabel("Amount (mol)")
plt.title(r"Equilibrium of $H_2 + I_2 \rightleftharpoons 2HI$ ($K = 15.6$)")
plt.grid(True, linestyle=":", alpha=0.6)
plt.legend()
plt.tight_layout()

plt.savefig("equilibrium.png", dpi=300)
plt.close()