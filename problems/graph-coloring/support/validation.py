import argparse
from parser import IOParser # for parsing input files

def validateColoring(inputProblemPath, inputResultPath):
    ''' Validate if the coloring in inputResultPath is valid for the graph in inputProblemPath. '''
    inputGraph = IOParser.parse2nx(inputProblemPath)
    colors = IOParser.parse_solution(inputResultPath)

    for u, v in inputGraph.edges:
        try:
            if colors[u] == colors[v]:  # adjacent cannot have the same color
                return False
        except KeyError:
            raise ValueError(f"Missing color for node {u} or {v}")
    return True


if __name__ == "__main__":  
    argParser = argparse.ArgumentParser()
    argParser.add_argument("inputProblem", type=str, help="Input file path of problem")
    argParser.add_argument("inputResult", type=str, help="Input file path of result")

    args = argParser.parse_args() # parse command line arguments

    is_valid = validateColoring(args.inputProblem, args.inputResult)
    if is_valid:
        print("Valid coloring")
    else:
        print("Invalid coloring")
