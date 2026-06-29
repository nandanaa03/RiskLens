from collections import deque


class BFS:

    @staticmethod
    def traverse(graph, start):

        visited = set()

        queue = deque([start])

        cluster = []

        while queue:

            node = queue.popleft()

            if node not in visited:

                visited.add(node)

                cluster.append(node)

                for neighbour in graph.get(node, []):

                    if neighbour not in visited:

                        queue.append(neighbour)

        return cluster