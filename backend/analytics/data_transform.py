import pandas as pd


class DataTransformer:

    @staticmethod
    def pivot_dataset(df):

        pivot_df = df.pivot_table(
            index="state",
            columns="indicator",
            values="nfhs5_total",
            aggfunc="mean"
        )

        pivot_df.reset_index(inplace=True)

        return pivot_df