import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


np.random.seed(42)


def exercise_1_matrix_operations() -> None:
    """Exercise 1: Determinant and inverse of a 3x3 matrix."""
    matrix = np.array(
        [
            [4, 7, 2],
            [3, 6, 1],
            [2, 5, 9],
        ]
    )

    determinant = np.linalg.det(matrix)
    inverse = np.linalg.inv(matrix)

    print("=== Exercise 1: Matrix Operations ===")
    print("Matrix:\n", matrix)
    print(f"Determinant: {determinant:.4f}")
    print("Inverse:\n", inverse)
    print()


def exercise_2_statistical_analysis() -> None:
    """Exercise 2: Mean, median, and standard deviation on random data."""
    data = np.random.rand(50)

    mean_value = np.mean(data)
    median_value = np.median(data)
    std_dev = np.std(data)

    print("=== Exercise 2: Statistical Analysis ===")
    print("Random data (50 values):\n", data)
    print(f"Mean: {mean_value:.4f}")
    print(f"Median: {median_value:.4f}")
    print(f"Standard deviation: {std_dev:.4f}")
    print()


def exercise_3_date_manipulation() -> None:
    """Exercise 3: Create and format January 2023 dates."""
    dates = np.arange("2023-01-01", "2023-02-01", dtype="datetime64[D]")
    formatted_dates = np.datetime_as_string(dates, unit="D")
    formatted_dates = np.char.replace(formatted_dates, "-", "/")

    print("=== Exercise 3: Date Manipulation ===")
    print("Original dates:")
    print(dates)
    print("Formatted dates (YYYY/MM/DD):")
    print(formatted_dates)
    print()


def exercise_4_data_manipulation() -> None:
    """Exercise 4: Conditional selection and aggregation with Pandas."""
    df = pd.DataFrame(np.random.randint(1, 101, size=(6, 4)), columns=["A", "B", "C", "D"])

    condition = df["A"] > 50
    selected_rows = df[condition]

    column_sums = df.sum()
    column_means = df.mean()

    print("=== Exercise 4: Data Manipulation with NumPy and Pandas ===")
    print("DataFrame:")
    print(df)
    print("\nRows where column A > 50:")
    print(selected_rows)
    print("\nColumn sums:")
    print(column_sums)
    print("\nColumn means:")
    print(column_means)
    print()


def exercise_5_image_representation() -> None:
    """Exercise 5: Explain and demonstrate image representation with arrays."""
    grayscale_image = np.array(
        [
            [0, 64, 128, 192, 255],
            [10, 70, 130, 190, 245],
            [20, 80, 140, 180, 235],
            [30, 90, 150, 170, 225],
            [40, 100, 160, 200, 215],
        ],
        dtype=np.uint8,
    )

    print("=== Exercise 5: Image Representation ===")
    print("A grayscale image can be represented as a 2D NumPy array.")
    print("Each value is an intensity from 0 (black) to 255 (white).")
    print("Example 5x5 grayscale image:")
    print(grayscale_image)
    print()


def exercise_6_hypothesis_testing() -> None:
    """Exercise 6: Basic hypothesis test using NumPy statistics."""
    productivity_before = np.random.normal(loc=50, scale=10, size=30)
    productivity_after = productivity_before + np.random.normal(loc=5, scale=3, size=30)

    differences = productivity_after - productivity_before
    mean_diff = np.mean(differences)
    std_diff = np.std(differences, ddof=1)
    se_diff = std_diff / np.sqrt(len(differences))

    # Approximate 95% confidence interval around mean difference.
    ci_low = mean_diff - 1.96 * se_diff
    ci_high = mean_diff + 1.96 * se_diff

    print("=== Exercise 6: Basic Hypothesis Testing ===")
    print("Hypothesis:")
    print("H0: The training program does not improve productivity (mean difference <= 0).")
    print("H1: The training program improves productivity (mean difference > 0).")
    print(f"Mean productivity difference (after - before): {mean_diff:.4f}")
    print(f"Std of differences: {std_diff:.4f}")
    print(f"Approx. 95% CI of mean difference: [{ci_low:.4f}, {ci_high:.4f}]")

    if ci_low > 0:
        print("Decision: Reject H0. Evidence suggests the training improved productivity.")
    else:
        print("Decision: Fail to reject H0. Evidence is not strong enough.")
    print()


def exercise_7_complex_array_comparison() -> None:
    """Exercise 7: Element-wise comparison between two arrays."""
    array_1 = np.array([5, 12, 7, 3, 19, 8])
    array_2 = np.array([4, 15, 7, 1, 14, 10])

    comparison = array_1 > array_2

    print("=== Exercise 7: Complex Array Comparison ===")
    print("Array 1:", array_1)
    print("Array 2:", array_2)
    print("Array 1 > Array 2:", comparison)
    print()


def exercise_8_time_series_manipulation() -> None:
    """Exercise 8: Generate and slice 2023 daily time series."""
    dates = np.arange("2023-01-01", "2024-01-01", dtype="datetime64[D]")

    jan_mar = dates[(dates >= np.datetime64("2023-01-01")) & (dates < np.datetime64("2023-04-01"))]
    apr_jun = dates[(dates >= np.datetime64("2023-04-01")) & (dates < np.datetime64("2023-07-01"))]
    jul_sep = dates[(dates >= np.datetime64("2023-07-01")) & (dates < np.datetime64("2023-10-01"))]
    oct_dec = dates[(dates >= np.datetime64("2023-10-01")) & (dates < np.datetime64("2024-01-01"))]

    print("=== Exercise 8: Time Series Data Manipulation ===")
    print(f"Total days in 2023 time series: {len(dates)}")
    print(f"January to March: {jan_mar[0]} -> {jan_mar[-1]} ({len(jan_mar)} days)")
    print(f"April to June: {apr_jun[0]} -> {apr_jun[-1]} ({len(apr_jun)} days)")
    print(f"July to September: {jul_sep[0]} -> {jul_sep[-1]} ({len(jul_sep)} days)")
    print(f"October to December: {oct_dec[0]} -> {oct_dec[-1]} ({len(oct_dec)} days)")
    print()


def exercise_9_data_conversion() -> None:
    """Exercise 9: Convert NumPy array to DataFrame and back."""
    np_array = np.array([[1, 2, 3], [4, 5, 6]])
    df = pd.DataFrame(np_array, columns=["col1", "col2", "col3"])
    back_to_np = df.to_numpy()

    print("=== Exercise 9: Data Conversion ===")
    print("Original NumPy array:")
    print(np_array)
    print("\nConverted to Pandas DataFrame:")
    print(df)
    print("\nConverted back to NumPy array:")
    print(back_to_np)
    print()


def exercise_10_basic_visualization() -> None:
    """Exercise 10: Plot random data with Matplotlib."""
    y = np.random.randint(0, 100, size=20)
    x = np.arange(1, len(y) + 1)

    plt.figure(figsize=(8, 4))
    plt.plot(x, y, marker="o", linestyle="-", color="tab:blue", label="Random values")
    plt.title("Exercise 10: Line Graph of Random Numbers")
    plt.xlabel("Index")
    plt.ylabel("Value")
    plt.grid(True, linestyle="--", alpha=0.5)
    plt.legend()
    plt.tight_layout()
    plt.show()


def main() -> None:
    exercise_1_matrix_operations()
    exercise_2_statistical_analysis()
    exercise_3_date_manipulation()
    exercise_4_data_manipulation()
    exercise_5_image_representation()
    exercise_6_hypothesis_testing()
    exercise_7_complex_array_comparison()
    exercise_8_time_series_manipulation()
    exercise_9_data_conversion()
    exercise_10_basic_visualization()


if __name__ == "__main__":
    main()
