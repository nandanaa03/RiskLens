import pandas as pd

from backend.algorithms.cluster import StateCluster

df = pd.read_csv("data/processed/risk_scores.csv")

clusters = StateCluster.get_clusters(df)

clustered_states = set()

print("\n========== STATE CLUSTERS ==========\n")

for i, cluster in enumerate(clusters, start=1):

    clustered_states.update(cluster)

    print(f"Cluster {i}")
    print(cluster)
    print()

# States with no neighbours
remaining = set(df["state"]) - clustered_states

for state in sorted(remaining):

    print(f"Cluster {len(clusters)+1}")
    print([state])
    print()
    clusters.append([state])