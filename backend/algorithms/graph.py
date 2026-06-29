class Graph:

    def __init__(self):
        self.graph = {}

    def add_edge(self, u, v):

        self.graph.setdefault(u, []).append(v)
        self.graph.setdefault(v, []).append(u)

    def get_graph(self):
        return self.graph