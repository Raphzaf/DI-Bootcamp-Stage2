"""
Week 5 - Day 2 - ExerciseXP
Statistical analysis exercises with SciPy.
"""

import scipy
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import stats


def exercise_1_basic_usage() -> None:
    """Exercise 1: Import SciPy and print its version."""
    print("Exercise 1: Basic Usage of SciPy")
    print(f"SciPy version: {scipy.__version__}")
    print("-" * 50)


def exercise_2_descriptive_statistics() -> None:
    """Exercise 2: Mean, median, variance, standard deviation."""
    data = np.array([12, 15, 13, 12, 18, 20, 22, 21])

    mean_value = np.mean(data)
    median_value = np.median(data)
    variance_value = np.var(data, ddof=1)
    std_dev_value = np.std(data, ddof=1)

    print("Exercise 2: Descriptive Statistics")
    print(f"Data: {data.tolist()}")
    print(f"Mean: {mean_value:.2f}")
    print(f"Median: {median_value:.2f}")
    print(f"Variance (sample): {variance_value:.2f}")
    print(f"Standard deviation (sample): {std_dev_value:.2f}")
    print("-" * 50)


def exercise_3_normal_distribution() -> None:
    """Exercise 3: Generate and plot a normal distribution."""
    np.random.seed(42)

    mean = 50
    std_dev = 10
    samples = np.random.normal(loc=mean, scale=std_dev, size=1000)

    x = np.linspace(mean - 4 * std_dev, mean + 4 * std_dev, 200)
    y = stats.norm.pdf(x, loc=mean, scale=std_dev)

    plt.figure(figsize=(8, 5))
    plt.hist(samples, bins=30, density=True, alpha=0.6, color="skyblue", label="Samples")
    plt.plot(x, y, "r-", linewidth=2, label="Normal PDF")
    plt.title("Exercise 3: Normal Distribution (mean=50, std=10)")
    plt.xlabel("Value")
    plt.ylabel("Density")
    plt.legend()
    plt.tight_layout()
    plt.savefig("exercise_3_distribution.png", dpi=150)
    plt.close()

    print("Exercise 3: Understanding Distributions")
    print("Normal distribution plot saved as exercise_3_distribution.png")
    print("-" * 50)


def exercise_4_t_test() -> None:
    """Exercise 4: Perform an independent t-test on two random datasets."""
    np.random.seed(42)

    data1 = np.random.normal(50, 10, 100)
    data2 = np.random.normal(60, 10, 100)

    t_stat, p_value = stats.ttest_ind(data1, data2)

    print("Exercise 4: T-Test Application")
    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.6f}")
    if p_value < 0.05:
        print("Result: Significant difference between groups (p < 0.05).")
    else:
        print("Result: No significant difference between groups (p >= 0.05).")
    print("-" * 50)


def exercise_5_linear_regression() -> None:
    """Exercise 5: Linear regression for house prices vs size."""
    house_sizes = np.array([50, 70, 80, 100, 120], dtype=float)
    house_prices = np.array([150000, 200000, 210000, 250000, 280000], dtype=float)

    slope, intercept, r_value, p_value, std_err = stats.linregress(house_sizes, house_prices)

    size_to_predict = 90
    predicted_price = slope * size_to_predict + intercept

    print("Exercise 5: Linear Regression Analysis")
    print(f"Slope: {slope:.2f}")
    print(f"Intercept: {intercept:.2f}")
    print(f"R-squared: {r_value ** 2:.4f}")
    print(f"P-value: {p_value:.6f}")
    print(f"Predicted price for {size_to_predict} m^2: {predicted_price:.2f}")
    print(
        "Interpretation: For each additional square meter, "
        f"the predicted price increases by about {slope:.2f} currency units."
    )
    print("-" * 50)


def exercise_6_anova() -> None:
    """Exercise 6: One-way ANOVA for fertilizer groups."""
    fertilizer_1 = [5, 6, 7, 6, 5]
    fertilizer_2 = [7, 8, 7, 9, 8]
    fertilizer_3 = [4, 5, 4, 3, 4]

    f_value, p_value = stats.f_oneway(fertilizer_1, fertilizer_2, fertilizer_3)

    print("Exercise 6: Understanding ANOVA")
    print(f"F-value: {f_value:.4f}")
    print(f"P-value: {p_value:.6f}")

    if p_value < 0.05:
        print("Conclusion: The fertilizers have significantly different effects.")
    else:
        print("Conclusion: No statistically significant difference among fertilizers.")

    print("If p-value were greater than 0.05:")
    print(
        "We would fail to reject the null hypothesis, meaning observed differences "
        "could be due to random variation rather than real fertilizer effects."
    )
    print("-" * 50)


def exercise_7_binomial_distribution() -> None:
    """Exercise 7 (Optional): Binomial probability example."""
    n = 10
    p = 0.5
    k = 5

    probability_exactly_5 = stats.binom.pmf(k, n, p)

    print("Exercise 7 (Optional): Probability Distributions")
    print(f"P(X = {k}) for {n} coin flips: {probability_exactly_5:.6f}")
    print("-" * 50)


def exercise_8_correlation_coefficients() -> None:
    """Exercise 8 (Optional): Pearson and Spearman correlations."""
    data = pd.DataFrame(
        {
            "age": [23, 25, 30, 35, 40],
            "income": [35000, 40000, 50000, 60000, 70000],
        }
    )

    pearson_corr, pearson_p = stats.pearsonr(data["age"], data["income"])
    spearman_corr, spearman_p = stats.spearmanr(data["age"], data["income"])

    print("Exercise 8 (Optional): Correlation Coefficients")
    print(f"Pearson correlation: {pearson_corr:.4f} (p-value={pearson_p:.6f})")
    print(f"Spearman correlation: {spearman_corr:.4f} (p-value={spearman_p:.6f})")
    print("-" * 50)


def main() -> None:
    exercise_1_basic_usage()
    exercise_2_descriptive_statistics()
    exercise_3_normal_distribution()
    exercise_4_t_test()
    exercise_5_linear_regression()
    exercise_6_anova()
    exercise_7_binomial_distribution()
    exercise_8_correlation_coefficients()


if __name__ == "__main__":
    main()
