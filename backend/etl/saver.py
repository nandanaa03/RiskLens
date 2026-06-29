from pathlib import Path


class DatasetSaver:

    @staticmethod
    def save_csv(df, output_path):

        output_path = Path(output_path)

        output_path.parent.mkdir(parents=True, exist_ok=True)

        df.to_csv(output_path, index=False)

        print(f"\nCleaned dataset saved to:\n{output_path}")