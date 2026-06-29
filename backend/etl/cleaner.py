import pandas as pd


class DataCleaner:

    @staticmethod
    def clean_text(df):

        text_columns = [
            "state",
            "state_code",
            "indicator"
        ]

        for column in text_columns:

            df[column] = (
                df[column]
                .fillna("")
                .astype(str)
                .str.strip()
            )

        return df

    @staticmethod
    def clean_numeric(df):

        numeric_columns = [
            "nfhs5_urban",
            "nfhs5_rural",
            "nfhs5_total",
            "nfhs4_total"
        ]

        for column in numeric_columns:

            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

        return df

    @staticmethod
    def remove_duplicates(df):

        return df.drop_duplicates()

    @staticmethod
    def fill_missing_values(df):

        numeric_columns = [
            "nfhs5_urban",
            "nfhs5_rural",
            "nfhs5_total",
            "nfhs4_total"
        ]

        for column in numeric_columns:

            median = df[column].median()

            df[column] = df[column].fillna(median)

        return df

    @staticmethod
    def run_pipeline(df):

        df = DataCleaner.clean_text(df)

        df = DataCleaner.clean_numeric(df)

        df = DataCleaner.remove_duplicates(df)

        df = DataCleaner.fill_missing_values(df)

        return df