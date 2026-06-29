import pandas as pd

from backend.analytics.risk_engine import RiskEngine


df = pd.read_csv(
    "data/processed/transformed_data.csv"
)

risk_df = RiskEngine.calculate(df)

risk_df = RiskEngine.categorize(risk_df)

print()

print(risk_df[

    [

        "state",

        "Risk Score",

        "Risk Level"

    ]

].sort_values(

    by="Risk Score",

    ascending=False

))

risk_df.to_csv(

    "data/processed/risk_scores.csv",

    index=False

)

print()

print("Risk Scores Generated Successfully.")