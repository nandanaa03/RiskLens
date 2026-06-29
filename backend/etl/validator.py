class DatasetValidator:

    REQUIRED_COLUMNS = [
        "state",
        "state_code",
        "indicator",
        "nfhs5_urban",
        "nfhs5_rural",
        "nfhs5_total",
        "nfhs4_total"
    ]

    @staticmethod
    def validate_columns(df):

        missing = []

        for column in DatasetValidator.REQUIRED_COLUMNS:

            if column not in df.columns:
                missing.append(column)

        if missing:
            raise ValueError(f"Missing Columns : {missing}")

        return True