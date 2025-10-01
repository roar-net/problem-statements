import networkx as nx


class IOParser:
    """Parser for DIMACS formatted graph files and solution files."""

    @staticmethod
    def parse2nx(file_path: str) -> nx.Graph:
        """Parse a DIMACS formatted file into a NetworkX graph."""
        edges = []
        num_vertices = 0
        num_edges = 0

        with open(file_path, "r") as f:
            for line in f:
                if not line.strip():
                    continue  # Skip empty lines
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

    @staticmethod
    def parse_solution(file_path: str) -> dict[int, int]:
        """Parse a solution file into a dictionary mapping vertices to colors."""
        with open(file_path, "r") as f:
            coloring = {}
            for line in f:
                if not line.strip():
                    continue  # Skip empty lines
                splitted = line.split()
                coloring[int(splitted[0])] = int(splitted[1])

        if not coloring:
            raise ValueError("No solution found in the file")

        return coloring
