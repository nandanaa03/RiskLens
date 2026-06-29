from backend.etl.loader import DatasetLoader
from backend.etl.validator import DatasetValidator
from backend.etl.cleaner import DataCleaner
from backend.etl.saver import DatasetSaver
from backend.utils.helpers import print_summary
from backend.utils.report import ETLReport

# ==============================
# File Paths
# ==============================

DATA_PATH = "data/raw/NFHS-5-States.csv"
OUTPUT_PATH = "data/processed/cleaned_data.csv"

# ==============================
# Load Dataset
# ==============================

print("\nLoading Dataset...\n")

loader = DatasetLoader(DATA_PATH)

df = loader.load_dataset()

# ==============================
# Validate Dataset
# ==============================

DatasetValidator.validate_columns(df)

print("Dataset Validation Successful\n")

# ==============================
# Dataset Summary
# ==============================

summary = loader.dataset_summary(df)

print_summary(summary)

# ==============================
# Data Cleaning
# ==============================

print("\nCleaning Dataset...\n")

clean_df = DataCleaner.run_pipeline(df)

# ==============================
# Save Clean Dataset
# ==============================

DatasetSaver.save_csv(
    clean_df,
    OUTPUT_PATH
)

# ==============================
# Generate ETL Report
# ==============================

report = ETLReport.generate(df, clean_df)

print("\n========== ETL REPORT ==========\n")

for key, value in report.items():
    print(f"{key:<25}: {value}")

# ==============================
# Preview Cleaned Dataset
# ==============================

print("\n========== CLEANED DATASET ==========\n")

print(clean_df.head())

print("\nDataset Shape:", clean_df.shape)

print("\nData Types:\n")

print(clean_df.dtypes)

print("\nMissing Values:\n")

print(clean_df.isnull().sum())

print("\nETL Pipeline Completed Successfully.")

from backend.analytics.data_transform import DataTransformer
from backend.analytics.explorer import DatasetExplorer

print("\nTransforming Dataset...\n")

pivot_df = DataTransformer.pivot_dataset(clean_df)

DatasetExplorer.dataset_info(pivot_df)

print("\nFirst Five Rows\n")

print(pivot_df.head())

pivot_df.to_csv(
    "data/processed/transformed_data.csv",
    index=False
)

print("\nTransformation Completed Successfully.")