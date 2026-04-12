import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import LabelEncoder, MinMaxScaler, StandardScaler


def load_titanic_dataset() -> pd.DataFrame:
	"""Load Titanic data from a stable public CSV source."""
	url = "https://raw.githubusercontent.com/datasciencedojo/datasets/master/titanic.csv"
	return pd.read_csv(url)


def show_missing_values(df: pd.DataFrame, title: str) -> None:
	missing = df.isna().sum()
	missing = missing[missing > 0].sort_values(ascending=False)
	print(f"\n{title}")
	if missing.empty:
		print("No missing values found.")
	else:
		print(missing)


def cap_outliers_iqr(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
	"""Cap outliers using IQR fences."""
	out = df.copy()
	for col in columns:
		q1 = out[col].quantile(0.25)
		q3 = out[col].quantile(0.75)
		iqr = q3 - q1
		low = q1 - 1.5 * iqr
		high = q3 + 1.5 * iqr
		out[col] = out[col].clip(lower=low, upper=high)
	return out


def main() -> None:
	df = load_titanic_dataset()
	print(f"Initial shape: {df.shape}")

	# Exercise 1: Duplicate Detection and Removal
	duplicate_count = df.duplicated().sum()
	print(f"\nExercise 1 - duplicate rows found: {duplicate_count}")
	before_rows = len(df)
	df = df.drop_duplicates().reset_index(drop=True)
	after_rows = len(df)
	print(f"Rows before removal: {before_rows}")
	print(f"Rows after removal:  {after_rows}")

	# Exercise 2: Handling Missing Values
	show_missing_values(df, "Exercise 2 - missing values before handling")

	# Strategy A: row removal where Embarked is missing (small amount usually)
	removed_rows = df["Embarked"].isna().sum()
	df = df.dropna(subset=["Embarked"]).reset_index(drop=True)
	print(f"\nDropped rows with missing Embarked: {removed_rows}")

	# Strategy B: numeric imputation for Age using median
	age_imputer = SimpleImputer(strategy="median")
	df["Age"] = age_imputer.fit_transform(df[["Age"]]).ravel()

	# Strategy C: fill constant value for Cabin because many values are missing
	df["Cabin"] = df["Cabin"].fillna("Unknown")

	# Optional: fill Fare if missing (dataset can have rare missing fares)
	df["Fare"] = df["Fare"].fillna(df["Fare"].median())

	show_missing_values(df, "Exercise 2 - missing values after handling")

	# Exercise 3: Feature Engineering
	df["FamilySize"] = df["SibSp"] + df["Parch"] + 1
	df["Title"] = df["Name"].str.extract(r",\s*([^\.]+)\.", expand=False).str.strip()
	df["Title"] = df["Title"].replace(
		{
			"Mlle": "Miss",
			"Ms": "Miss",
			"Mme": "Mrs",
			"Lady": "Rare",
			"Countess": "Rare",
			"Capt": "Rare",
			"Col": "Rare",
			"Don": "Rare",
			"Dr": "Rare",
			"Major": "Rare",
			"Rev": "Rare",
			"Sir": "Rare",
			"Jonkheer": "Rare",
			"Dona": "Rare",
		}
	)

	# Encode Title here as requested in exercise 3
	title_encoder = LabelEncoder()
	df["TitleEncoded"] = title_encoder.fit_transform(df["Title"])

	# Exercise 4: Outlier Detection and Handling
	outlier_cols = ["Fare", "Age"]
	print("\nExercise 4 - quantiles before outlier handling")
	print(df[outlier_cols].quantile([0.95, 0.98, 0.99, 1.0]))

	fig, axes = plt.subplots(2, 2, figsize=(12, 8))
	df["Fare"].plot(kind="box", ax=axes[0, 0], title="Fare Boxplot (Before)")
	df["Age"].plot(kind="box", ax=axes[0, 1], title="Age Boxplot (Before)")
	df["Fare"].plot(kind="hist", bins=30, ax=axes[1, 0], title="Fare Histogram (Before)")
	df["Age"].plot(kind="hist", bins=30, ax=axes[1, 1], title="Age Histogram (Before)")
	plt.tight_layout()
	plt.show()

	# Quantile capping and log transform for Fare
	fare_cap = df["Fare"].quantile(0.98)
	age_cap = df["Age"].quantile(0.99)
	df["FareCapped"] = df["Fare"].clip(upper=fare_cap)
	df["AgeCapped"] = df["Age"].clip(upper=age_cap)
	df["FareLog"] = np.log(df["FareCapped"] + 1)

	# Alternative IQR handling for comparison
	df_iqr = cap_outliers_iqr(df, ["Fare", "Age"])

	print("\nExercise 4 - quantiles after capping")
	print(df[["FareCapped", "AgeCapped"]].quantile([0.95, 0.98, 0.99, 1.0]))

	# Exercise 7: Data Transformation for Age Feature
	bins = [0, 12, 18, 60, 100]
	labels = ["child", "teen", "adult", "senior"]
	df["AgeGroup"] = pd.cut(df["AgeCapped"], bins=bins, labels=labels, include_lowest=True)
	age_group_dummies = pd.get_dummies(df["AgeGroup"], prefix="AgeGroup", dtype=int)

	# Exercise 6: Feature Encoding (remaining categorical columns)
	categorical_nominal = ["Sex", "Embarked", "Title", "AgeGroup"]
	encoded_nominal = pd.get_dummies(df[categorical_nominal], prefix=categorical_nominal, dtype=int)

	# If any ordinal variable existed, LabelEncoder would be used.
	# Example shown on Pclass as an ordinal feature.
	ordinal_encoder = LabelEncoder()
	df["PclassLabel"] = ordinal_encoder.fit_transform(df["Pclass"])

	# Merge encoded columns
	df_model = pd.concat([df, encoded_nominal, age_group_dummies], axis=1)

	# Exercise 5: Data Standardization and Normalization
	# Apply after outlier handling and encoding steps to avoid distortion.
	standard_features = ["AgeCapped", "SibSp", "Parch", "FamilySize"]
	minmax_features = ["FareCapped", "FareLog"]

	standard_scaler = StandardScaler()
	minmax_scaler = MinMaxScaler()

	df_model[[f"{c}_std" for c in standard_features]] = standard_scaler.fit_transform(df_model[standard_features])
	df_model[[f"{c}_mm" for c in minmax_features]] = minmax_scaler.fit_transform(df_model[minmax_features])

	print("\nFinal dataset shape (with engineered features):", df_model.shape)
	print("\nPreview of processed data:")
	print(df_model.head())


if __name__ == "__main__":
	# Keep default warnings simple for exercise readability.
	pd.options.mode.chained_assignment = None
	main()
