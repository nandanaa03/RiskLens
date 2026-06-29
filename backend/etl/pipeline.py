import re
import pandas as pd

from backend.etl.loader import DatasetLoader
from backend.etl.cleaner import DataCleaner
from backend.etl.validator import DatasetValidator


class ETLPipeline:

    # Mapping of NFHS indicator numbers
    INDICATOR_MAP = {
        88: "Obesity_W",
        89: "Obesity_M",
        92: "Anaemia_Child",
        95: "Anaemia_W",
        101: "BloodSugar_W",
        104: "BloodSugar_M",
        107: "Hypertension_W",
        110: "Hypertension_M",
    }

    @staticmethod
    def extract_indicator_number(text):

        match = re.match(r"^\s*(\d+)\.", str(text))

        if match:
            return int(match.group(1))

        return None

    @staticmethod
    def run(dataset_path):

        loader = DatasetLoader(dataset_path)

        df = loader.load_dataset()

        DatasetValidator.validate_columns(df)

        df = DataCleaner.run_pipeline(df)

        # Remove India aggregate
        df = df[df["state"] != "India"].copy()

        # Get indicator number
        df["indicator_number"] = df["indicator"].apply(
            ETLPipeline.extract_indicator_number
        )

        # Keep only required indicators
        df = df[
            df["indicator_number"].isin(
                ETLPipeline.INDICATOR_MAP.keys()
            )
        ]

        # Rename indicators
        df["Metric"] = df["indicator_number"].map(
            ETLPipeline.INDICATOR_MAP
        )

        # Convert long → wide
        df = df.pivot_table(
            index="state",
            columns="Metric",
            values="nfhs5_total",
            aggfunc="first"
        )

        df = df.reset_index()

        # Fill missing values
        df = df.fillna(df.median(numeric_only=True))

        summary = {
            "states_loaded": len(df),
            "columns": len(df.columns)
        }

        return df, summary