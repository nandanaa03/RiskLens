from backend.etl.pipeline import ETLPipeline

from backend.analytics.risk_engine import RiskEngine

from backend.algorithms.cluster import StateCluster

df = ETLPipeline.run("data/raw/NFHS-5-States.csv")

df = RiskEngine.run(df)

df = StateCluster.attach_clusters(df)

print(df[[
    "state",
    "Risk Score",
    "Risk Level",
    "Cluster"
]].head())

print()

print(df["Cluster"].value_counts())