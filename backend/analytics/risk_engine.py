import numpy as np
import pandas as pd


class RiskEngine:

    WEIGHTS = {
        "Obesity_W": 0.20,
        "Obesity_M": 0.15,
        "Anaemia_Child": 0.20,
        "Anaemia_W": 0.15,
        "BloodSugar_W": 0.10,
        "BloodSugar_M": 0.10,
        "Hypertension_W": 0.05,
        "Hypertension_M": 0.05,
    }

    @staticmethod
    def normalize(df):

        df = df.copy()

        for column in RiskEngine.WEIGHTS.keys():

            minimum = df[column].min()

            maximum = df[column].max()

            if maximum == minimum:

                df[column + "_Norm"] = 0

            else:

                df[column + "_Norm"] = (
                    (df[column] - minimum) /
                    (maximum - minimum)
                )

        return df

    @staticmethod
    def calculate_risk_score(df):

        df = RiskEngine.normalize(df)

        score = 0

        for column, weight in RiskEngine.WEIGHTS.items():

            score += df[column + "_Norm"] * weight

        df["Risk Score"] = score.round(4)

        return df

    @staticmethod
    def assign_risk_level(df):

        q1 = df["Risk Score"].quantile(0.25)
        q2 = df["Risk Score"].quantile(0.50)
        q3 = df["Risk Score"].quantile(0.75)

        def level(score):

            if score >= q3:
                return "Critical"

            elif score >= q2:
                return "High"

            elif score >= q1:
                return "Moderate"

            else:
                return "Low"

        df["Risk Level"] = df["Risk Score"].apply(level)

        return df

    @staticmethod
    def find_top_driver(df):

        drivers = []

        for _, row in df.iterrows():

            contribution = {}

            for column, weight in RiskEngine.WEIGHTS.items():

                contribution[column] = (
                    row[column + "_Norm"] * weight
                )

            driver = max(contribution, key=contribution.get)

            drivers.append(driver)

        df["Top Driver"] = drivers

        return df

    @staticmethod
    def run(df):

        df = RiskEngine.calculate_risk_score(df)

        df = RiskEngine.assign_risk_level(df)

        df = RiskEngine.find_top_driver(df)

        return df