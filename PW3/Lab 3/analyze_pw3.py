"""End-to-end analysis for Practical Work 3.

Run from the repository root with the ``cspc`` environment active:
    python "PW3/Lab 3/analyze_pw3.py"

Expected inputs beside this script: heart.csv and chemicals_cancer.csv.
"""

from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


HERE = Path(__file__).resolve().parent
CONTINUOUS = ["age", "chol", "trestbps", "thalach"]


def check_file(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Missing {path.name}. Put the Moodle dataset next to {Path(__file__).name}."
        )


def heart_analysis():
    path = HERE / "heart.csv"
    check_file(path)
    df = pd.read_csv(path)
    required = set(CONTINUOUS + ["target"])
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"heart.csv is missing columns: {sorted(missing)}")

    print("HEART DATA")
    print("Shape:", df.shape)
    print(df.head(), "\n")
    print(df[CONTINUOUS].describe(), "\n")

    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, column in zip(axes.flat, CONTINUOUS):
        values = df[column].dropna()
        ax.hist(values, bins="auto", edgecolor="white")
        ax.set(title=column, xlabel=column, ylabel="Count")
        # Shapiro-Wilk is limited to 5,000 observations; sample deterministically if needed.
        test_values = values.sample(5000, random_state=1) if len(values) > 5000 else values
        result = stats.shapiro(test_values)
        print(f"{column}: Shapiro W={result.statistic:.4f}, p={result.pvalue:.4g}")
        print(f"  skew={stats.skew(values):.3f}; inspect histogram and QQ plot as well")
    fig.tight_layout()
    fig.savefig(HERE / "heart_distributions.png", dpi=180)
    plt.close(fig)

    # QQ plots supplement the Shapiro test: a tiny p-value alone can flag trivial
    # departures from normality in a large sample.
    fig, axes = plt.subplots(2, 2, figsize=(10, 7))
    for ax, column in zip(axes.flat, CONTINUOUS):
        stats.probplot(df[column].dropna(), dist="norm", plot=ax)
        ax.set_title(f"Normal Q-Q: {column}")
    fig.tight_layout()
    fig.savefig(HERE / "heart_qqplots.png", dpi=180)
    plt.close(fig)

    diseased = df.loc[df.target == 1, "thalach"].dropna()
    healthy = df.loc[df.target == 0, "thalach"].dropna()
    group_normality = []
    for label, group in [("Disease", diseased), ("Healthy", healthy)]:
        sample = group.sample(5000, random_state=1) if len(group) > 5000 else group
        result = stats.shapiro(sample)
        group_normality.append(result.pvalue > 0.05)
        print(f"{label} thalach normality: Shapiro W={result.statistic:.4f}, p={result.pvalue:.4g}")
    normal_enough = all(group_normality)
    if normal_enough:
        test = stats.ttest_ind(diseased, healthy, equal_var=False)
        method = "Welch two-sample t-test"
    else:
        test = stats.mannwhitneyu(diseased, healthy, alternative="two-sided")
        method = "Mann-Whitney U test"
    print("\nTHALACH GROUP COMPARISON")
    print(f"Method: {method}; statistic={test.statistic:.4f}, p={test.pvalue:.6g}")
    group_summaries = []
    for label, values in [("Disease", diseased), ("Healthy", healthy)]:
        mean = values.mean()
        sem = stats.sem(values)
        ci = stats.t.interval(0.95, len(values) - 1, loc=mean, scale=sem)
        group_summaries.append((label, mean, sem, ci))
        print(f"{label}: n={len(values)}, mean={mean:.2f}, SEM={sem:.2f}, 95% CI=({ci[0]:.2f}, {ci[1]:.2f})")
    fig, ax = plt.subplots(figsize=(6, 4))
    means = [item[1] for item in group_summaries]
    errors = [item[3][1] - item[1] for item in group_summaries]
    ax.bar([item[0] for item in group_summaries], means, yerr=errors, capsize=6, color=["#4472C4", "#ED7D31"])
    ax.set(ylabel="Maximum heart rate (thalach)", title="Mean thalach with 95% confidence intervals")
    fig.tight_layout()
    fig.savefig(HERE / "thalach_by_target.png", dpi=180)
    plt.close(fig)

    pair = df[["age", "thalach"]].dropna()
    rho, pvalue = stats.spearmanr(pair.age, pair.thalach)
    print(f"\nAGE vs THALACH: Spearman rho={rho:.4f}, p={pvalue:.6g}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(pair.age, pair.thalach, alpha=0.65, edgecolors="none")
    ax.set(xlabel="Age (years)", ylabel="Maximum heart rate", title=f"Age vs thalach (Spearman rho={rho:.2f})")
    fig.tight_layout()
    fig.savefig(HERE / "age_vs_thalach.png", dpi=180)
    plt.close(fig)

    proportions = df.target.value_counts(normalize=True)
    entropy = -(proportions * np.log2(proportions)).sum()
    print(f"\nBONUS target entropy: {entropy:.4f} bits (maximum 1 bit for two balanced classes)")


def residual_correlation(data, x, y, controls):
    """Partial Pearson correlation after linear adjustment for control columns."""
    values = data[[x, y] + controls].dropna()
    design = np.column_stack([np.ones(len(values)), values[controls].to_numpy()])
    residual_x = values[x].to_numpy() - design @ np.linalg.lstsq(design, values[x].to_numpy(), rcond=None)[0]
    residual_y = values[y].to_numpy() - design @ np.linalg.lstsq(design, values[y].to_numpy(), rcond=None)[0]
    r = stats.pearsonr(residual_x, residual_y).statistic
    degrees_of_freedom = len(values) - len(controls) - 2
    t_statistic = r * np.sqrt(degrees_of_freedom / (1 - r**2))
    p_value = 2 * stats.t.sf(abs(t_statistic), degrees_of_freedom)
    return r, p_value


def chemical_analysis():
    path = HERE / "chemicals_cancer.csv"
    check_file(path)
    df = pd.read_csv(path)
    print("\nCHEMICAL EXPOSURE DATA")
    print("Shape:", df.shape)
    print(df.describe(), "\n")
    for chemical in ["benzene", "cadmium"]:
        r, p = stats.pearsonr(df[chemical], df.malignancy)
        print(f"Naive {chemical} vs malignancy: Pearson r={r:.4f}, p={p:.3g}")

    controls = ["pollution_index", "age"]
    for chemical in ["benzene", "cadmium"]:
        r, p = residual_correlation(df, chemical, "malignancy", controls)
        print(f"Adjusted for pollution_index and age, {chemical}: partial r={r:.4f}, p={p:.3g}")

    # Compare patients in a narrow pollution-index band to reduce confounding.
    subset = df[df.pollution_index.between(45, 55)]
    print(f"\nPollution-index 45-55 slice (n={len(subset)}):")
    for chemical in ["benzene", "cadmium"]:
        r, p = stats.pearsonr(subset[chemical], subset.malignancy)
        print(f"  {chemical}: r={r:.4f}, p={p:.3g}")

    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    for ax, chemical in zip(axes, ["benzene", "cadmium"]):
        ax.scatter(df[chemical], df.malignancy, c=df.pollution_index, cmap="viridis", alpha=0.7, edgecolors="none")
        ax.set(xlabel=chemical, ylabel="Malignancy", title=f"{chemical} vs malignancy")
    fig.tight_layout()
    fig.savefig(HERE / "chemical_associations.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    if (HERE / "heart.csv").exists():
        heart_analysis()
    else:
        print("heart.csv is missing; skipping heart-dataset analysis for now.")
    chemical_analysis()
