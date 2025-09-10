import argparse
from parser import IOParser

def validateColoring(inputProblemPath, inputResultPath):
    inputGraph = IOParser.parse2nx(inputProblemPath)
    colors = IOParser.parse_solution(inputResultPath)

    for u, v in inputGraph.edges:
        try:
            if colors[u] == colors[v]:
                return False
        except KeyError:
            raise ValueError(f"Missing color for node {u} or {v}")
    return True


if __name__ == "__main__":  
    argParser = argparse.ArgumentParser()
    argParser.add_argument("inputProblem", type=str, help="Input file path of problem")
    argParser.add_argument("inputResult", type=str, help="Input file path of result")

    args = argParser.parse_args()

    is_valid = validateColoring(args.inputProblem, args.inputResult)
    if is_valid:
        print("Valid coloring")
    else:
        print("Invalid coloring")
