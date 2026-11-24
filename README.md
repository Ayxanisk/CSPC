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

# PW3 — Data, distributions, testing, and causation

Run the complete analysis from its folder, following the same relative-path style as the earlier practical-work scripts:

```bash
conda activate cspc
cd "PW3/Lab 3"
python analyze_pw3.py
```

The script reads `heart.csv` and `chemicals_cancer.csv` from the current folder, prints the numerical results, and regenerates the plots there. It uses pandas, NumPy, SciPy, and Matplotlib.

## Session 1 — Heart data

The heart table has **303 patients and 14 columns**. The four continuous columns used below are age, cholesterol (`chol`), resting blood pressure (`trestbps`), and maximum heart rate (`thalach`).

| Variable | Distribution and normality verdict |
| --- | --- |
| Age | Roughly bell-shaped and close to normal, with a slight left skew. Shapiro–Wilk gives W = 0.9865, p = 0.0061, so exact normality is rejected at the 5% level; the histogram and Q–Q plot show that the departure is modest. |
| Cholesterol (`chol`) | Not normal: it is strongly right-skewed, with several unusually high values. The Q–Q plot bends sharply in the upper tail. W = 0.9473, p = 5.9 × 10⁻⁹. |
| Resting blood pressure (`trestbps`) | Not normal: it has a right tail and high outliers. W = 0.9665, p = 1.8 × 10⁻⁶, and the Q–Q plot departs from the reference line in the upper tail. |
| Maximum heart rate (`thalach`) | Roughly unimodal, but not well described by a normal distribution: the lower tail and extreme values depart from the Q–Q line. W = 0.9765, p = 7.0 × 10⁻⁵. |

The Shapiro–Wilk test checks exact normality, so I read it together with the plots and skewness rather than treating its p-value alone as a measure of practical importance.

![Heart-variable histograms](PW3/Lab%203/heart_distributions.png)

![Heart-variable normal Q–Q plots](PW3/Lab%203/heart_qqplots.png)

## Session 2 — Heart data

Patients with heart disease (target = 1, n = 139) had a lower average maximum heart rate (**139.26 bpm**, SEM 1.92; 95% CI 135.47–143.05) than healthy patients (target = 0, n = 164; **158.38 bpm**, SEM 1.50; 95% CI 155.42–161.34). The disease group's `thalach` values are reasonably consistent with normality (Shapiro p = 0.352), while the healthy group's are not (p = 0.00054). I used a two-sided Mann–Whitney U test rather than assuming normally distributed values in both groups. The difference is statistically clear (U = 5,806.5, p = 1.86 × 10⁻¹³). The confidence intervals also show the groups' means are well separated; this agrees with the test. The bars below show the means and 95% confidence intervals.

![Mean maximum heart rate with 95% confidence intervals](PW3/Lab%203/thalach_by_target.png)

Age and maximum heart rate have a **moderate negative rank correlation** (Spearman ρ = −0.392, p = 1.51 × 10⁻¹²): in this sample, older patients tend to reach a lower maximum heart rate. This is an association, not evidence that age alone caused the difference.

![Age and maximum heart rate scatter plot](PW3/Lab%203/age_vs_thalach.png)

For the bonus, target's Shannon entropy is **0.995 bits** out of a maximum of 1 bit. The two classes are nearly balanced, so guessing the more common class provides little advantage over a 50/50 guess.

## Chemical-exposure mystery

The synthetic table has **1,000 records**. The naive Pearson correlations with malignancy are:

| Chemical | Pearson correlation with malignancy |
| --- | ---: |
| Benzene | 0.385 |
| Cadmium | 0.880 |

Read alone, these values make cadmium look much more suspicious. But cadmium is almost a proxy for the area's pollution index (r = 0.982), and malignancy also rises with the pollution index (r = 0.895). Benzene is almost unrelated to the pollution index (r = 0.054).

To account for pollution as a possible third factor, I hold its value approximately constant by keeping only the 96 people whose pollution index is between 45 and 55. Within this group, benzene remains associated with malignancy (r = 0.668, p < 0.001), while cadmium is not (r = −0.037, p = 0.723). So the strong overall cadmium association disappears when we compare people with similar pollution exposure.

The synthetic dataset's intended cause is **benzene**. Cadmium looked guilty because it tracks pollution, which itself tracks malignancy; among people with similar pollution exposure, the cadmium relationship disappears while the benzene relationship remains. This supports benzene as the culprit in this synthetic example. For real observational data, this kind of comparison is evidence about confounding, not proof of causation.

![Chemical levels and malignancy; point color shows pollution index](PW3/Lab%203/chemical_associations.png)

## PW3 data source

Heart Disease (Cleveland), UCI Machine Learning Repository, available at <https://archive.ics.uci.edu/dataset/45/heart+disease>. The Moodle copy supplied for the practical is used here. The synthetic chemical dataset is supplied with the practical.
