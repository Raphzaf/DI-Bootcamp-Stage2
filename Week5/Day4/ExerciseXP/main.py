from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# ------------------------------
# Exercise 1: Theory
# ------------------------------
print("Exercise 1: Understanding Data Visualization")
print(
    "1) Data visualization is important because it helps us quickly understand patterns, trends, "
    "outliers, and relationships in data that are difficult to see in raw tables."
)
print(
    "2) A line graph is mainly used to show how a value changes over time or across an ordered "
    "sequence, making trends and changes easy to follow."
)
print("-" * 80)


# ------------------------------
# Exercise 2: Line plot (temperature)
# ------------------------------
temperatures = [72, 74, 76, 80, 82, 78, 75]
days = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

plt.figure(figsize=(8, 4))
plt.plot(days, temperatures, marker="o", linewidth=2, color="tab:blue")
plt.xlabel("Day")
plt.ylabel("Temperature (°F)")
plt.title("Temperature Variation Over a Week")
plt.grid(alpha=0.3)
plt.tight_layout()
plt.show()


# ------------------------------
# Exercise 3: Bar chart (monthly sales)
# ------------------------------
months = ["Jan", "Feb", "Mar", "Apr", "May"]
sales = [5000, 5500, 6200, 7000, 7500]

plt.figure(figsize=(8, 4))
plt.bar(months, sales, color="teal")
plt.xlabel("Month")
plt.ylabel("Sales Amount ($)")
plt.title("Monthly Sales for a Retail Store")
plt.tight_layout()
plt.show()


# ------------------------------
# Exercises 4-6: Student Mental Health dataset
# ------------------------------
def find_existing_dataset() -> Path | None:
    """Find the CSV file in common local locations near this script."""
    base_dir = Path(__file__).resolve().parent
    candidates = [
        base_dir / "Student Mental health.csv",
        base_dir / "Student Mental health" / "Student Mental health.csv",
        base_dir / "student_mental_health.csv",
        base_dir / "Student_Mental_health.csv",
    ]

    for path in candidates:
        if path.exists():
            return path

    # Fallback: search recursively for any csv containing both words in the filename.
    for path in base_dir.rglob("*.csv"):
        name = path.name.lower()
        if "student" in name and "mental" in name:
            return path
    return None


def pick_column(df_: pd.DataFrame, options: list[str]) -> str:
    """Return the first matching column from a list of possible names."""
    for col in options:
        if col in df_.columns:
            return col
    raise KeyError(
        f"None of the expected columns were found. Tried: {options}. "
        f"Available columns: {list(df_.columns)}"
    )


def yes_no_to_int(series: pd.Series) -> pd.Series:
    mapping = {
        "yes": 1,
        "no": 0,
        "y": 1,
        "n": 0,
        "1": 1,
        "0": 0,
        "true": 1,
        "false": 0,
    }
    return (
        series.astype(str)
        .str.strip()
        .str.lower()
        .map(mapping)
    )


dataset_path = find_existing_dataset()
if dataset_path is None:
    print("Dataset not found for exercises 4-6.")
    print(
        "Please download and extract 'Student Mental health.zip' in "
        "Week5/Day4/ExerciseXP, then run this script again."
    )
else:
    print(f"Using dataset: {dataset_path}")
    df = pd.read_csv(dataset_path)

    # ------------------------------
    # Exercise 4: Histogram of CGPA
    # ------------------------------
    cgpa_col = pick_column(
        df,
        [
            "CGPA",
            "What is your CGPA?",
            "What is your CGPA",
        ],
    )

    plt.figure(figsize=(9, 4))
    sns.histplot(
        x=df[cgpa_col].astype(str),
        color="coral",
        shrink=0.8,
    )
    plt.xlabel("CGPA")
    plt.ylabel("Count")
    plt.title("Distribution of Students' CGPA")
    plt.xticks(rotation=30)
    plt.tight_layout()
    plt.show()

    # ---------------------------------------------
    # Exercise 5: Anxiety levels across genders
    # ---------------------------------------------
    anxiety_col = pick_column(
        df,
        [
            "Do you have Anxiety?",
            "Do you have anxiety?",
            "Do you have Anxiety",
        ],
    )
    gender_col = pick_column(
        df,
        [
            "Choose your gender",
            "Gender",
            "What is your gender?",
        ],
    )

    anxiety_numeric = yes_no_to_int(df[anxiety_col])
    anxiety_by_gender = (
        pd.DataFrame({"gender": df[gender_col], "anxiety": anxiety_numeric})
        .dropna()
        .groupby("gender", as_index=False)["anxiety"]
        .mean()
    )

    plt.figure(figsize=(8, 4))
    sns.barplot(
        data=anxiety_by_gender,
        x="gender",
        y="anxiety",
        palette="Set2",
        hue="gender",
        legend=False,
    )
    plt.xlabel("Gender")
    plt.ylabel("Proportion with Anxiety")
    plt.title("Proportion of Students with Anxiety by Gender")
    plt.ylim(0, 1)
    plt.tight_layout()
    plt.show()

    # -----------------------------------------------------
    # Exercise 6: Age vs panic attacks (scatter)
    # -----------------------------------------------------
    age_col = pick_column(
        df,
        [
            "Age",
            "age",
        ],
    )
    panic_col = pick_column(
        df,
        [
            "Do you have Panic Attacks?",
            "Do you have Panic Attack?",
            "Do you have Panic attack?",
            "Do you have panic attack?",
            "Do you have Panic Attack",
        ],
    )

    age_values = pd.to_numeric(df[age_col], errors="coerce")
    panic_numeric = yes_no_to_int(df[panic_col])
    scatter_df = pd.DataFrame({"Age": age_values, "Panic": panic_numeric}).dropna()

    plt.figure(figsize=(8, 4))
    sns.scatterplot(
        data=scatter_df,
        x="Age",
        y="Panic",
        alpha=0.7,
        s=70,
        color="purple",
    )
    plt.xlabel("Age")
    plt.ylabel("Panic Attacks (No=0, Yes=1)")
    plt.title("Relationship Between Age and Panic Attacks")
    plt.yticks([0, 1], ["No", "Yes"])
    plt.tight_layout()
    plt.show()
