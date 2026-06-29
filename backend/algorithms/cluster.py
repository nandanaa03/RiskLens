from backend.algorithms.graph import Graph
from backend.algorithms.bfs import BFS


class StateCluster:

    THRESHOLD = 0.05

    @staticmethod
    def build_graph(df):

        graph = Graph()

# Add every state as a node
        for state in df["state"]:
            graph.graph.setdefault(state, [])

        for i in range(len(df)):

            state1 = df.iloc[i]["state"]
            score1 = df.iloc[i]["Risk Score"]
            level1 = df.iloc[i]["Risk Level"]

            for j in range(i + 1, len(df)):

                state2 = df.iloc[j]["state"]
                score2 = df.iloc[j]["Risk Score"]
                level2 = df.iloc[j]["Risk Level"]

                if level1 != level2:
                    continue

                if abs(score1 - score2) <= StateCluster.THRESHOLD:
                    graph.add_edge(state1, state2)

        return graph.get_graph()

    @staticmethod
    def attach_clusters(df):

        graph = StateCluster.build_graph(df)

        visited = set()

        cluster_number = 1

        cluster_map = {}

        for node in graph:

            if node not in visited:

                cluster = BFS.traverse(graph, node)

                visited.update(cluster)

                for state in cluster:

                    cluster_map[state] = cluster_number

                cluster_number += 1

        df["Cluster"] = df["state"].map(cluster_map)

        if df["Cluster"].isna().any():
            raise ValueError("Some states were not assigned to any cluster.")

        df["Cluster"] = df["Cluster"].astype(int)

        return df