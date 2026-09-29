## PW1 - Lab A: Reproducible Foundations

**What I built:**
- Built a radioactive decay simulation using pure Python loops and vectorized NumPy code.
- Set up conda environment tracking, .gitignore rules, and full Git workflow.

## Results & Performance Comparison
- **N0**: 200,000 atoms
- **Pure-Python loop execution time**: 11.11722 seconds
- **NumPy execution time**:          0.0003 seconds
- **Speed-up factor**: 42860.36x faster than pure-Python loop

**Tests:** all passing? yes

**Conclusion:**
- Vectorized operations with NumPy dramatically increase execution speed compared to standard Python loops.
- Automated unit tests with pytest ensure code correctness, while Conda environment files maintain reproducibility across different machines.

**Reproducibility test (Stretch Goal):**
- Tested code on a partner's machine: environment built seamlessly without modifications, and all pytest cases passed without errors.

## PW1 Lab B
**What the data showed:** The data demonstrates an exponential decay process over time, with the count decreasing rapidly at first and then leveling off. 
**Match with analytical law:** The observed data points closely match the analytical decay curve ($N_{0}e^{-\lambda t}$), confirming that the analytical law accurately describes the observed phenomenon.
**Snakemake Pipeline:** The Snakemake pipeline automates the generation of the plot, ensuring `figure.png` is only rebuilt if the input dataset (`decay_observed.csv`) or the python script (`plot.py`) changes.x



## PW2 Lab A -- Motion from Tracking Data

**What I built:**
- Computed velocity and acceleration from noisy position measurements (`freefall.csv`) using `np.gradient` finite-difference methods[cite: 1].
- Reconstructed velocity and position profiles back from acceleration via numerical integration with `scipy.integrate.cumulative_trapezoid`[cite: 1].
- Created a 3-panel figure (`motion.png`) displaying position, velocity, and acceleration alongside the reference line $g = -9.81 \text{ m/s}^2$[cite: 1].

## Results & Analysis
- **Mean Acceleration:** ~$-9.8 \text{ m/s}^2$, confirming free-fall dynamics under standard gravity[cite: 1].
- **Noise Characteristics:** While position measurements appear smooth, taking successive numerical derivatives amplifies high-frequency noise, making the acceleration curve significantly noisier[cite: 1].
- **Reconstruction:** Integrating acceleration recovers the general trends of velocity and position when anchored with proper initial values ($v_0, y_0$)[cite: 1].

**Tests:** all passing? yes

**Conclusion:**
- `np.gradient` provides an efficient way to compute numerical derivatives, but double differentiation is highly sensitive to measurement noise[cite: 1].
- Numerical integration via `scipy.integrate.cumulative_trapezoid` effectively smoothes out high-frequency noise, successfully recovering velocity and trajectory[cite: 1].