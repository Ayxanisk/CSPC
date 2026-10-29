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



# PW2 — Lab B: Optimization in Chemistry[cite: 1]

## Overview
This section focuses on the practical application of numerical optimization and differentiation methods to chemical problems: fitting reaction kinetics, determining chemical equilibrium compositions, and detecting the equivalence point in an acid-base titration[cite: 1].

---

## Part 2: Three Routes to a Minimum[cite: 1]

### 2A. Easy Convex Function ($f(x) = (x-3)^2 + 1$)[cite: 1]
For this quadratic function with a single global minimum at $x = 3$, three optimization approaches were evaluated starting from $x_0 = 0$[cite: 1]:
1. **Gradient Descent (by hand)**: Converged reliably to $x \approx 3.0000$ using a fixed step size[cite: 1].
2. **Newton's Method (`scipy.optimize.newton` on $f'(x) = 0$)**: Converged to $x = 3.0000$ in very few iterations due to constant positive curvature ($f''(x) = 2$)[cite: 1].
3. **SLSQP (`scipy.optimize.minimize`)**: Accurately located the minimum at $x = 3.0000$[cite: 1].

*Takeaway*: On smooth, convex landscapes, all three algorithms easily find the correct global minimum[cite: 1, 2].

### 2B. A Harder Landscape ($g(x) = x^4 - 3x^2 + x + 5$)[cite: 1]
This function features multiple stationary points (two local minima and one local maximum)[cite: 1]. Method behavior strongly depends on the initial guess $x_0$[cite: 1, 2]:

* **Starting from $x_0 = 0$**:
  * **Gradient Descent**: Steps downhill along the negative gradient toward the negative local minimum[cite: 1].
  * **Newton's Method**: Finds the nearest stationary point at $x \approx 0.17$[cite: 1]. Evaluating the second derivative reveals $g''(x) < 0$, confirming that Newton's method landed on a **local maximum**, not a minimum[cite: 1].
  * **SLSQP**: Converges to a local minimum depending on gradient evaluation[cite: 1].
* **Starting from $x_0 = 2$**:
  * All three methods fall into the basin of attraction of the right-hand minimum ($x \approx 1.14$, where $g''(x) > 0$)[cite: 1].

*Key lesson*: On non-convex landscapes, algorithm selection and initial starting values are crucial[cite: 2]. Because Newton's method solves $g'(x) = 0$, checking the sign of the curvature ($g''$) is necessary to distinguish minima from maxima[cite: 1].

---

## Part 3: Chemistry 1 — Fit a Reaction Rate[cite: 2]

Non-linear least squares regression was applied to noisy concentration measurements over time following first-order kinetics $C(t) = C_0 e^{-kt}$ by minimizing the residual sum of squares[cite: 2]:
$$\text{error}(k) = \sum_{i} \left(C_{\text{measured}, i} - C_0 e^{-kt_i}\right)^2$$[cite: 2]

* **Initial concentration $C_0$**: Set to the first measured data point[cite: 2].
* **Optimization routine**: SLSQP (`scipy.optimize.minimize`) with bound constraints $k \in [0, 5]$ and initial estimate $x_0 = 0.5$[cite: 2].
* **Results**: The optimal rate constant converged to $k \approx 0.25 \, \text{s}^{-1}$[cite: 2].
* The fitted exponential decay curve accurately traces the experimental data (`kinetics.png`)[cite: 2].

---

## Part 4: Chemistry 2 — Chemical Equilibrium[cite: 2]

For the gas-phase reaction:
$$\text{H}_2 + \text{I}_2 \rightleftharpoons 2\text{HI}$$[cite: 2]
starting with $1\text{ mol } \text{H}_2$ and $1\text{ mol } \text{I}_2$, the amounts at extent $x$ are $n_{\text{H}_2} = 1 - x$, $n_{\text{I}_2} = 1 - x$, and $n_{\text{HI}} = 2x$[cite: 2]. The system satisfies the equilibrium relation[cite: 2]:
$$K = \frac{(2x)^2}{(1-x)(1-x)} \implies k_{\text{imbalance}}(x) = \frac{4x^2}{(1-x)^2} - K = 0$$[cite: 2]

The extent $x$ was determined using two numerical techniques[cite: 2]:
1. **Newton's method (`scipy.optimize.newton`)**: Direct root-finding on $k_{\text{imbalance}}(x) = 0$[cite: 2].
2. **SLSQP minimization (`scipy.optimize.minimize`)**: Minimizing $(k_{\text{imbalance}}(x))^2$ subject to $x \in [0, 0.999]$[cite: 2].

* **Comparison**: Both methods converged to identical equilibrium extents within numerical tolerance[cite: 2].
* **Equilibrium Composition**:
  * $n_{\text{H}_2} = 1 - x$[cite: 2]
  * $n_{\text{I}_2} = 1 - x$[cite: 2]
  * $n_{\text{HI}} = 2x$[cite: 2]
* Species amounts as a function of reaction progress and the marked equilibrium point are displayed in `equilibrium.png`[cite: 2].

---

## Part 5 (Bonus): Chemistry 3 — Titration Equivalence Point[cite: 2]

In an acid-base titration, the equivalence point represents the volume of titrant where pH changes most rapidly (the maximum of the first derivative $\frac{dpH}{dV}$)[cite: 2].

* **Numerical Analysis**:
  1. The derivative curve was calculated via central differences using `np.gradient(pH, V)`[cite: 3].
  2. The point of steepest increase was identified via `np.argmax(slope)`[cite: 3].
* **Results**: The equivalence point was located at $V_{\text{equiv}} \approx 50.0\text{ mL}$, coinciding with the inflection point of the titration curve and the sharp peak of the derivative[cite: 3].
* The titration curve and its derivative are plotted side-by-side in `titration.png`[cite: 3].