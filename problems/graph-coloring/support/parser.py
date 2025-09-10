import networkx as nx


class DimacsParser:

    @staticmethod
    def parse2nx(file_path):
        edges = []
        num_vertices = 0
        num_edges = 0

        with open(file_path, "r") as f:
            for line in f:
                if not line.strip():
                    continue
                splitted = line.split()
                if splitted[0] == "e":
                    edges.append((int(splitted[1]), int(splitted[2])))
                elif splitted[0] == "c":
                    pass
                elif splitted[0] == "p":
                    if splitted[1] != "edge":
                        raise ValueError(f"Unsupported problem type {splitted[1]}")
                    num_vertices = int(splitted[2])
                    num_edges = int(splitted[3])
                else:
                    raise ValueError(f"Unknown line type {splitted[0]}")

        g = nx.Graph(edges)
        if g.number_of_nodes() != num_vertices:
            raise ValueError("Number of vertices does not match the specified count")
        if g.number_of_edges() != num_edges:
            raise ValueError("Number of edges does not match the specified count")

        return g


# DimacsParser.parse2nx("./data/1-FullIns_3/1-FullIns_3.col")
