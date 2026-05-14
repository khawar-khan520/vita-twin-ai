import networkx as nx

class MentalHealthGraph:
    def __init__(self):
        self.graph = nx.DiGraph()
        self.build_graph()

    def build_graph(self):
        # Nodes + relationships
        edges = [
            ("low_sleep", "stress"),
            ("stress", "burnout"),
            ("isolation", "depression"),
            ("exercise", "improves_mood"),
            ("poor_sleep", "fatigue"),
        ]

        self.graph.add_edges_from(edges)

    def get_relationships(self):
        return list(self.graph.edges())

    def explain_path(self, factor):
        paths = []

        for edge in self.graph.edges():
            if factor in edge:
                paths.append(edge)

        return paths


# test
if __name__ == "__main__":
    kg = MentalHealthGraph()

    print("Graph edges:")
    print(kg.get_relationships())

    print("\nExplanation for 'stress':")
    print(kg.explain_path("stress"))