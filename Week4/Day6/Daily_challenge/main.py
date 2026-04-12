from pathlib import Path

import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import MinMaxScaler, StandardScaler


LOCAL_DATASET = Path(__file__).with_name("ds_salaries.csv")
DATASET_URL = "https://raw.githubusercontent.com/amankharwal/Website-data/master/ds_salaries.csv"


def load_dataset(local_path: Path = LOCAL_DATASET, url: str = DATASET_URL) -> pd.DataFrame:
	"""Load dataset from local CSV, or download from URL if local file is missing."""
	if local_path.exists():
		return pd.read_csv(local_path)

	print(f"Local dataset not found at {local_path}. Downloading from URL...")
	return pd.read_csv(url)


def normalize_salary(df: pd.DataFrame) -> pd.DataFrame:
	"""Add a Min-Max normalized salary column scaled between 0 and 1."""
	if "salary" not in df.columns:
		raise KeyError("The dataset must contain a 'salary' column.")

	scaler = MinMaxScaler()
	df = df.copy()
	df["salary_normalized"] = scaler.fit_transform(df[["salary"]])
	return df


def reduce_dimensions_with_pca(df: pd.DataFrame, n_components: int = 2) -> pd.DataFrame:
	"""Reduce dataset features with PCA and return a DataFrame of principal components."""
	# Create a model-ready matrix: one-hot encode categoricals and keep numerics.
	feature_matrix = pd.get_dummies(df, drop_first=True)

	# Standardization is important before PCA so large-scale columns do not dominate.
	scaled_features = StandardScaler().fit_transform(feature_matrix)

	pca = PCA(n_components=n_components, random_state=42)
	reduced = pca.fit_transform(scaled_features)
	explained_variance = pca.explained_variance_ratio_.sum()

	reduced_df = pd.DataFrame(
		reduced,
		columns=[f"PC{i + 1}" for i in range(n_components)],
		index=df.index,
	)

	print(f"\nPCA completed with {n_components} components.")
	print(f"Total explained variance: {explained_variance:.2%}")
	return reduced_df


def aggregate_salary_by_experience(df: pd.DataFrame) -> pd.DataFrame:
	"""Group by experience level and compute average/median salaries."""
	if "experience_level" not in df.columns:
		raise KeyError("The dataset must contain an 'experience_level' column.")

	grouped = (
		df.groupby("experience_level")["salary"]
		.agg(average_salary="mean", median_salary="median")
		.sort_values("average_salary")
	)

	# Common mapping for ds_salaries dataset labels.
	level_map = {
		"EN": "Junior (Entry)",
		"MI": "Mid-level",
		"SE": "Senior",
		"EX": "Executive",
	}

	grouped = grouped.reset_index()
	grouped["experience_level_label"] = grouped["experience_level"].map(level_map).fillna(
		grouped["experience_level"]
	)
	return grouped[["experience_level", "experience_level_label", "average_salary", "median_salary"]]


def main() -> None:
	df = load_dataset()

	print("Dataset preview:")
	print(df.head())
	print(f"\nShape: {df.shape}")

	normalized_df = normalize_salary(df)
	print("\nSalary normalization (first 5 rows):")
	print(normalized_df[["salary", "salary_normalized"]].head())

	reduced_df = reduce_dimensions_with_pca(normalized_df, n_components=2)
	print("\nReduced feature set (first 5 rows):")
	print(reduced_df.head())

	salary_by_experience = aggregate_salary_by_experience(normalized_df)
	print("\nAverage and median salary by experience level:")
	print(salary_by_experience.to_string(index=False))


if __name__ == "__main__":
	main()
