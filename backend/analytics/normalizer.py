import pandas as pd


class DataNormalizer:

    @staticmethod
    def min_max(series):

        minimum = series.min()

        maximum = series.max()

        if minimum == maximum:
            return series

        return (series - minimum) / (maximum - minimum)