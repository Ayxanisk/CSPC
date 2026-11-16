# PW3 — Data, distributions, testing, and causation

Run the complete analysis from the repository root:

```bash
conda activate cspc
python "PW3/Lab 3/analyze_pw3.py"
```

The script reads both CSV files from `PW3/Lab 3/`, prints the numerical results, and regenerates the plots in that folder. It uses pandas, NumPy, SciPy, and Matplotlib.

## Session 1 — Heart data

The heart table has **303 patients and 14 columns**. The four continuous columns used below are age, cholesterol (`chol`), resting blood pressure (`trestbps`), and maximum heart rate (`thalach`).

| Variable | Distribution and normality verdict |
| --- | --- |
| Age | Roughly bell-shaped and close to normal, with a slight left skew. Shapiro–Wilk gives W = 0.9865, p = 0.0061, so exact normality is rejected at the 5% level; the histogram and Q–Q plot show that the departure is modest. |
| Cholesterol (`chol`) | Not normal: it is strongly right-skewed, with several unusually high values. The Q–Q plot bends sharply in the upper tail. W = 0.9473, p = 5.9 × 10⁻⁹. |
| Resting blood pressure (`trestbps`) | Not normal: it has a right tail and high outliers. W = 0.9665, p = 1.8 × 10⁻⁶, and the Q–Q plot departs from the reference line in the upper tail. |
| Maximum heart rate (`thalach`) | Roughly unimodal, but not well described by a normal distribution: the lower tail and extreme values depart from the Q–Q line. W = 0.9765, p = 7.0 × 10⁻⁵. |

The Shapiro–Wilk test checks exact normality, so I read it together with the plots and skewness rather than treating its p-value alone as a measure of practical importance.

![Heart-variable histograms](Lab%203/heart_distributions.png)

![Heart-variable normal Q–Q plots](Lab%203/heart_qqplots.png)

## Session 2 — Heart data

Patients with heart disease (target = 1, n = 139) had a lower average maximum heart rate (**139.26 bpm**, SEM 1.92; 95% CI 135.47–143.05) than healthy patients (target = 0, n = 164; **158.38 bpm**, SEM 1.50; 95% CI 155.42–161.34). The disease group's `thalach` values are reasonably consistent with normality (Shapiro p = 0.352), while the healthy group's are not (p = 0.00054). I used a two-sided Mann–Whitney U test rather than assuming normally distributed values in both groups. The difference is statistically clear (U = 5,806.5, p = 1.86 × 10⁻¹³). The confidence intervals also show the groups' means are well separated; this agrees with the test. The bars below show the means and 95% confidence intervals.

![Mean maximum heart rate with 95% confidence intervals](Lab%203/thalach_by_target.png)

Age and maximum heart rate have a **moderate negative rank correlation** (Spearman ρ = −0.392, p = 1.51 × 10⁻¹²): in this sample, older patients tend to reach a lower maximum heart rate. This is an association, not evidence that age alone caused the difference.

![Age and maximum heart rate scatter plot](Lab%203/age_vs_thalach.png)

For the bonus, target's Shannon entropy is **0.995 bits** out of a maximum of 1 bit. The two classes are nearly balanced, so guessing the more common class provides little advantage over a 50/50 guess.

## Chemical-exposure mystery

The synthetic table has **1,000 records**. The naive Pearson correlations with malignancy are:

| Chemical | Pearson correlation with malignancy |
| --- | ---: |
| Benzene | 0.385 |
| Cadmium | 0.880 |

Read alone, these values make cadmium look much more suspicious. But cadmium is almost a proxy for the area's pollution index (r = 0.982), and malignancy also rises with the pollution index (r = 0.895). Benzene is almost unrelated to the pollution index (r = 0.054).

I adjusted for both pollution index and age by regressing each chemical and malignancy on those two variables, then correlating the residuals. Benzene's partial correlation remains strong (r = 0.759, p = 3.47 × 10⁻¹⁸⁸); cadmium's falls to essentially zero (r = 0.007, p = 0.828). As a second check, among 96 people with a similar pollution index (45–55), benzene remains associated with malignancy (r = 0.668, p < 0.001), while cadmium does not (r = −0.037, p = 0.723).

The synthetic dataset's intended cause is **benzene**. Cadmium looked guilty because it tracks pollution, which itself tracks malignancy; once that shared factor is controlled, the cadmium relationship disappears and the benzene relationship remains. This conclusion is about how this synthetic dataset was constructed; correlation analysis by itself does not establish a causal effect in real patients.

![Chemical levels and malignancy; point color shows pollution index](Lab%203/chemical_associations.png)

## Data source

Heart Disease (Cleveland), UCI Machine Learning Repository, available at <https://archive.ics.uci.edu/dataset/45/heart+disease>. The Moodle copy supplied for the practical is used here. The synthetic chemical dataset is supplied with the practical.
