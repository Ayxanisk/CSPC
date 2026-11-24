"""End-to-end analysis for Practical Work 3.

Run from the repository root with the ``cspc`` environment active:
    python "PW3/Lab 3/analyze_pw3.py"

Expected inputs beside this script: heart.csv and chemicals_cancer.csv.
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy import stats


CONTINUOUS = ["age", "chol", "trestbps", "thalach"]

def heart_analysis():
    df = pd.read_csv("heart.csv")
    print("--------------------------HEART DATA--------------------------")
    print("---------------")
    print("Shape:", df.shape)
    print("---------------")
    print(df.head(), "\n")
    print(df[CONTINUOUS].describe(), "\n")

    hist_fig, hist_axes = plt.subplots(2, 2, figsize=(10, 7))
    qq_fig, qq_axes = plt.subplots(2, 2, figsize=(10, 7))

    for hist_ax, qq_ax, column in zip(hist_axes.flat, qq_axes.flat, CONTINUOUS):
        values = df[column].dropna()
        hist_ax.hist(values, bins="auto", edgecolor="white")
        hist_ax.set(title=column, xlabel=column, ylabel="Count")
                        
        stats.probplot(values, dist="norm", plot=qq_ax)
        qq_ax.set_title(f"Normal Q-Q: {column}")

        result = stats.shapiro(values)
        print(f"{column}: Shapiro W={result.statistic:.4f}, p={result.pvalue:.4g}")
        print(f"  skew={stats.skew(values):.3f}; inspect histogram and QQ plot as well")

    hist_fig.tight_layout()
    hist_fig.savefig("heart_distributions.png", dpi=180)
    plt.close(hist_fig)

    qq_fig.tight_layout()
    qq_fig.savefig("heart_qqplots.png", dpi=180)
    plt.close(qq_fig)

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
    fig.savefig("thalach_by_target.png", dpi=180)
    plt.close(fig)

    pair = df[["age", "thalach"]].dropna()
    rho, pvalue = stats.spearmanr(pair.age, pair.thalach)
    print(f"\nAGE vs THALACH: Spearman rho={rho:.4f}, p={pvalue:.6g}")
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.scatter(pair.age, pair.thalach, alpha=0.65, edgecolors="none")
    ax.set(xlabel="Age (years)", ylabel="Maximum heart rate", title=f"Age vs thalach (Spearman rho={rho:.2f})")
    fig.tight_layout()
    fig.savefig("age_vs_thalach.png", dpi=180)
    plt.close(fig)

    proportions = df.target.value_counts(normalize=True)
    entropy = -(proportions * np.log2(proportions)).sum()
    print(f"\nBONUS target entropy: {entropy:.4f} bits (maximum 1 bit for two balanced classes)")


def chemical_analysis():
    df = pd.read_csv("chemicals_cancer.csv")
    print("\nCHEMICAL EXPOSURE DATA")
    print("Shape:", df.shape)
    print(df.describe(), "\n")
    for chemical in ["benzene", "cadmium"]:
        r, p = stats.pearsonr(df[chemical], df.malignancy)
        print(f"Naive {chemical} vs malignancy: Pearson r={r:.4f}, p={p:.3g}")

    # Hold pollution index approximately constant by keeping only a narrow band.
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
    fig.savefig("chemical_associations.png", dpi=180)
    plt.close(fig)


if __name__ == "__main__":
    heart_analysis()
    chemical_analysis()
