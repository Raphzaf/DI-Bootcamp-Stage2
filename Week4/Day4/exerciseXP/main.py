"""
Week 4 - Day 4 - ExerciseXP
Comprehensive solutions for Exercises 1 to 10.

How to run:
1) Install dependencies (once):
   pip install pandas matplotlib seaborn openpyxl
2) Run:
   python main.py

Notes:
- Some Kaggle datasets require local files (downloaded manually from Kaggle).
- Set file paths in KAGGLE_DATASETS below before running those parts.
"""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


# -----------------------------
# Configuration
# -----------------------------

BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "outputs"
OUTPUT_DIR.mkdir(exist_ok=True)

# Update these paths after downloading datasets from Kaggle.
KAGGLE_DATASETS = {
	"sleep_americans": BASE_DIR / "data" / "how_much_sleep_do_americans_really_get.csv",
	"mental_health": BASE_DIR / "data" / "global_trends_mental_health_disorder.csv",
	"credit_card": BASE_DIR / "data" / "credit_card_approvals.csv",
	"iris": BASE_DIR / "data" / "Iris.csv",
}

# Exercise 8: Titanic train.csv from GitHub mirror.
TITANIC_TRAIN_URL = "https://raw.githubusercontent.com/agconti/kaggle-titanic/master/data/train.csv"

# Exercise 10: Sample JSON URL.
JSON_URL = "https://jsonplaceholder.typicode.com/posts"


# -----------------------------
# Utility functions
# -----------------------------

def print_title(title: str) -> None:
	print("\n" + "=" * 80)
	print(title)
	print("=" * 80)


def classify_column(series: pd.Series) -> str:
	"""
	Classify a pandas column as qualitative or quantitative.
	Rule of thumb:
	- Numeric columns -> quantitative
	- Object/category/bool/datetime -> qualitative for this assignment context
	"""
	if pd.api.types.is_numeric_dtype(series):
		return "quantitative"
	return "qualitative"


def classification_report(df: pd.DataFrame, dataset_name: str) -> pd.DataFrame:
	rows = []
	for col in df.columns:
		col_type = classify_column(df[col])
		if col_type == "quantitative":
			reason = "Numeric values that can be measured and summarized statistically."
		else:
			reason = "Represents categories, labels, text, booleans, or non-numeric descriptors."

		rows.append(
			{
				"dataset": dataset_name,
				"column": col,
				"pandas_dtype": str(df[col].dtype),
				"classification": col_type,
				"reason": reason,
			}
		)
	return pd.DataFrame(rows)


def preview_and_describe(df: pd.DataFrame, name: str, n: int = 5) -> None:
	print_title(f"Dataset Preview - {name}")
	print(df.head(n))

	print("\nShape:", df.shape)
	print("Columns:", list(df.columns))
	print("\nData types:")
	print(df.dtypes)
	print("\nMissing values per column:")
	print(df.isnull().sum())


# -----------------------------
# Exercise 1
# -----------------------------

def exercise_1_intro_report() -> None:
	print_title("Exercise 1 - Introduction to Data Analysis Report")

	report = """
What is data analysis?
Data analysis is the process of collecting, cleaning, transforming, and interpreting data to
extract meaningful insights and support decision-making. It combines statistics, domain
knowledge, and visualization to answer specific questions.

Why is data analysis important in modern contexts?
In modern organizations, data is generated continuously from apps, transactions, sensors,
websites, and social platforms. Data analysis helps organizations identify patterns, detect
problems early, forecast trends, and make evidence-based decisions instead of relying only
on intuition.

Three areas where data analysis is applied:
1. Healthcare:
   Hospitals analyze patient records and treatment outcomes to improve diagnosis,
   personalize care, and optimize resource allocation.
2. Finance:
   Banks and fintech companies use analysis for credit scoring, fraud detection, risk
   modeling, and customer segmentation.
3. E-commerce and Marketing:
   Companies analyze customer behavior, conversions, and campaign performance to
   improve targeting, retention, and product recommendations.
""".strip()

	print(report)
	(OUTPUT_DIR / "exercise_1_report.txt").write_text(report, encoding="utf-8")


# -----------------------------
# Exercise 2 and 3
# -----------------------------

def exercise_2_and_3_kaggle_loading_and_types() -> None:
	print_title("Exercise 2 and 3 - Load Kaggle Datasets, Preview, and Classify Data Types")

	all_reports = []

	for dataset_name, file_path in KAGGLE_DATASETS.items():
		if not file_path.exists():
			print(f"Skipped {dataset_name}: file not found at {file_path}")
			continue

		df = pd.read_csv(file_path)
		preview_and_describe(df, dataset_name)

		report_df = classification_report(df, dataset_name)
		all_reports.append(report_df)

		print("\nColumn classification:")
		print(report_df[["column", "classification", "reason"]])

	if all_reports:
		merged = pd.concat(all_reports, ignore_index=True)
		merged.to_csv(OUTPUT_DIR / "exercise_2_3_type_classification.csv", index=False)
		print("\nSaved combined type classification to outputs/exercise_2_3_type_classification.csv")


# -----------------------------
# Exercise 4
# -----------------------------

def exercise_4_iris_types() -> None:
	print_title("Exercise 4 - Iris Dataset Qualitative vs Quantitative")

	iris_path = KAGGLE_DATASETS["iris"]
	if not iris_path.exists():
		print(f"Skipped Exercise 4: Iris file not found at {iris_path}")
		return

	iris_df = pd.read_csv(iris_path)
	preview_and_describe(iris_df, "iris")

	iris_report = classification_report(iris_df, "iris")
	print("\nIris type classification:")
	print(iris_report[["column", "classification", "reason"]])

	iris_report.to_csv(OUTPUT_DIR / "exercise_4_iris_type_report.csv", index=False)


# -----------------------------
# Exercise 5
# -----------------------------

def exercise_5_observation_skills() -> None:
	print_title("Exercise 5 - Observation Skills (Sleep Dataset)")

	sleep_path = KAGGLE_DATASETS["sleep_americans"]
	if not sleep_path.exists():
		print(f"Skipped Exercise 5: Sleep file not found at {sleep_path}")
		return

	sleep_df = pd.read_csv(sleep_path)
	preview_and_describe(sleep_df, "sleep_americans")

	print("\nInteresting column candidates for analysis:")
	print(
		"- Trend analysis: date/time-related columns and average_sleep_duration\n"
		"- Group comparison: age_group, gender, employment_status, region\n"
		"- Health relation: stress_level, physical_activity, caffeine_intake, sleep_quality"
	)


# -----------------------------
# Exercise 6 and 7
# -----------------------------

def exercise_6_structured_vs_unstructured() -> None:
	print_title("Exercise 6 - Structured vs Unstructured Data")

	examples = {
		"A company's financial reports stored in an Excel file": "Structured",
		"Photographs uploaded to a social media platform": "Unstructured",
		"A collection of news articles on a website": "Unstructured",
		"Inventory data in a relational database": "Structured",
		"Recorded interviews from a market research study": "Unstructured",
	}

	for source, data_type in examples.items():
		print(f"- {source}: {data_type}")


def exercise_7_transformation_methods() -> None:
	print_title("Exercise 7 - Methods to Convert Unstructured Data to Structured")

	methods = {
		"Travel blog posts": (
			"Use NLP to extract entities (location, date, sentiment, activities) and store them "
			"in a table with columns like post_id, location, sentiment_score, and tags."
		),
		"Audio recordings of customer service calls": (
			"Apply speech-to-text transcription, then use text mining to capture issue type, "
			"resolution status, call duration, and customer sentiment into structured columns."
		),
		"Handwritten brainstorming notes": (
			"Use OCR to convert handwriting to text, then classify ideas into categories and "
			"store as rows with fields such as topic, priority, owner, and due date."
		),
		"Video tutorial on cooking": (
			"Extract transcript and key frames, then label steps, ingredients, and timing into "
			"a structured recipe/process table."
		),
	}

	for source, method in methods.items():
		print(f"- {source}: {method}")


# -----------------------------
# Exercise 8
# -----------------------------

def exercise_8_import_titanic_from_github() -> pd.DataFrame | None:
	print_title("Exercise 8 - Import Titanic train.csv from GitHub")
	try:
		titanic_df = pd.read_csv(TITANIC_TRAIN_URL)
		print(titanic_df.head())
		titanic_df.to_csv(OUTPUT_DIR / "exercise_8_titanic_train_preview.csv", index=False)
		return titanic_df
	except Exception as exc:
		print(f"Could not load Titanic data from URL: {exc}")
		return None


# -----------------------------
# Exercise 9
# -----------------------------

def exercise_9_export_dataframe() -> None:
	print_title("Exercise 9 - Export DataFrame to Excel and JSON")

	simple_df = pd.DataFrame(
		{
			"name": ["Alice", "Bob", "Charlie"],
			"age": [25, 30, 22],
			"city": ["New York", "Paris", "Tel Aviv"],
		}
	)
	print(simple_df)

	excel_path = OUTPUT_DIR / "exercise_9_simple_dataframe.xlsx"
	json_path = OUTPUT_DIR / "exercise_9_simple_dataframe.json"

	simple_df.to_excel(excel_path, index=False)
	simple_df.to_json(json_path, orient="records", indent=2)

	print(f"Saved Excel file to: {excel_path}")
	print(f"Saved JSON file to: {json_path}")


# -----------------------------
# Exercise 10
# -----------------------------

def exercise_10_read_json_from_url() -> None:
	print_title("Exercise 10 - Read JSON Data from URL")
	try:
		json_df = pd.read_json(JSON_URL)
		print(json_df.head())
		json_df.to_csv(OUTPUT_DIR / "exercise_10_json_preview.csv", index=False)
	except Exception as exc:
		print(f"Could not load JSON data from URL: {exc}")


# -----------------------------
# Statistical analysis + visualizations (Notebook-style workflow)
# -----------------------------

def create_basic_stats_and_plots() -> None:
	"""
	Demonstrates mean/median/mode and basic visualizations, aligned with the notebook task.
	Uses Titanic dataset from Exercise 8 if available.
	"""
	print_title("Notebook-style Analysis - Stats and Visualizations")

	try:
		df = pd.read_csv(TITANIC_TRAIN_URL)
	except Exception as exc:
		print(f"Skipped stats/plots: could not load Titanic URL ({exc})")
		return

	if "Age" in df.columns:
		age_series = df["Age"].dropna()
		print("Age mean:", age_series.mean())
		print("Age median:", age_series.median())
		print("Age mode:", age_series.mode().tolist())

		plt.figure(figsize=(8, 5))
		sns.histplot(age_series, bins=20, kde=True)
		plt.title("Titanic Age Distribution")
		plt.xlabel("Age")
		plt.ylabel("Frequency")
		plt.tight_layout()
		plt.savefig(OUTPUT_DIR / "hist_age_titanic.png")
		plt.close()

	if "Pclass" in df.columns:
		plt.figure(figsize=(6, 4))
		df["Pclass"].value_counts().sort_index().plot(kind="bar")
		plt.title("Passenger Count by Class")
		plt.xlabel("Passenger Class")
		plt.ylabel("Count")
		plt.tight_layout()
		plt.savefig(OUTPUT_DIR / "bar_pclass_titanic.png")
		plt.close()

	print("Saved visualizations in outputs/ folder.")


def main() -> None:
	exercise_1_intro_report()
	exercise_2_and_3_kaggle_loading_and_types()
	exercise_4_iris_types()
	exercise_5_observation_skills()
	exercise_6_structured_vs_unstructured()
	exercise_7_transformation_methods()
	exercise_8_import_titanic_from_github()
	exercise_9_export_dataframe()
	exercise_10_read_json_from_url()
	create_basic_stats_and_plots()


if __name__ == "__main__":
	main()
