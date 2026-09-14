import time
from decay import simulate, simulate_loop

N0 = 200000
lam = 0.05
dt = 0.05
steps = 200

t0 = time.perf_counter()
simulate_loop(N0, lam, dt=dt, steps=steps)
t1 = time.perf_counter()
time_loop = t1 - t0

t0 = time.perf_counter()
simulate(N0, lam, dt=dt, steps=steps)
t1 = time.perf_counter()
time_numpy = t1 - t0

speedup = time_loop / time_numpy

print(f"Pure-Python loop time: {time_loop:.4f} seconds")
print(f"NumPy time:            {time_numpy:.4f} seconds")
print(f"NumPy is {speedup:.2f}x faster than pure-Python loop.")