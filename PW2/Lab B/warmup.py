"""
PW2 Lab B Part 2 -- three routes to a minimum.

Compare gradient descent, Newton, and SLSQP on two functions:
  2A: f(x) = (x-3)**2 + 1          (easy, one minimum at x=3)
  2B: g(x) = x**4 - 3*x**2 + x + 5 (harder, several stationary points)
Run:  python warmup.py
"""
import numpy as np
from scipy.optimize import newton, minimize

# ---------- 2A: easy convex function ----------
def f(x):   return (x-3)**2 + 1
def df(x):  return 2*(x-3)
def d2f(x): return 2.0

# TODO 2A: minimise f three ways from x0=0 and print each result:
#   (1) gradient descent by hand (loop x = x - lr*df(x) until the step is tiny)
x_gd = 0.0
lr = 0.1
for _ in range(100):
    x_gd = x_gd - lr * df(x_gd)
#   (2) scipy.optimize.newton(df, x0, fprime=d2f)
x_newton = newton(df, x0=0.0, fprime=d2f)
#   (3) scipy.optimize.minimize(f, x0, method="SLSQP")
res_slsqp = minimize(f, x0=0.0, method="SLSQP")

print("--- 2A Results ---")
print(f"Gradient Descent: x = {x_gd:.4f}")
print(f"Newton's Method:  x = {x_newton:.4f}")
print(f"SLSQP Minimizer:  x = {res_slsqp.x[0]:.4f}\n")

# ---------- 2B: harder landscape ----------
def g(x):   return x**4 - 3*x**2 + x + 5
def dg(x):  return 4*x**3 - 6*x + 1
def d2g(x): return 12*x**2 - 6

# TODO 2B: run the same three methods on g, from x0=0 AND from x0=2.
def run_2b(x0):
    print(f"--- 2B Results (x0 = {x0}) ---")
    
    # 1. Gradient descent
    x_gd = x0
    lr = 0.01
    for _ in range(1000):
        x_gd = x_gd - lr * dg(x_gd)
    print(f"Gradient Descent: x = {x_gd:.4f}")
    
    # 2. Newton's method
    try:
        x_new = newton(dg, x0=x0, fprime=d2g)
        curvature = d2g(x_new)
        kind = "Minimum" if curvature > 0 else "Maximum"
        print(f"Newton's Method:  x = {x_new:.4f} (g'' = {curvature:.2f} -> {kind})")
    except Exception as e:
        print(f"Newton's Method:  Failed ({e})")
        
    # 3. SLSQP
    res = minimize(g, x0=x0, method="SLSQP")
    print(f"SLSQP Minimizer:  x = {res.x[0]:.4f}\n")

run_2b(x0=0.0)
run_2b(x0=2.0)