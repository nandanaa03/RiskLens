import pandas as pd
from pathlib import Path
from backend.utils.logger import logger

class DatasetLoader:

    def __init__(self, file_path: str):
        self.file_path = Path(file_path)

    def load_dataset(self):

        if not self.file_path.exists():
            raise FileNotFoundError(
                f"Dataset not found : {self.file_path}"
            )

        df = pd.read_csv(self.file_path, encoding="utf-8-sig")

# Remove extra spaces from headers immediately
        df.columns = df.columns.str.strip()
        logger.info(f"Loading dataset from {self.file_path}")
        return df

    def dataset_summary(self, df):

        summary = {
            "Rows": df.shape[0],
            "Columns": df.shape[1],
            "Duplicate Rows": df.duplicated().sum(),
            "Missing Values": int(df.isnull().sum().sum())
        }
        logger.info("Dataset summary generated")
        return summary