import pandas as pd

from backend.analytics.recommendation_engine import RecommendationEngine


risk_df = pd.read_csv(
    "data/processed/risk_scores.csv"
)

recommendation_df = RecommendationEngine.generate(risk_df)

recommendation_df.to_csv(
    "data/processed/recommendations.csv",
    index=False
)

print("\nRecommendations Generated Successfully.\n")

print(recommendation_df.head(10))