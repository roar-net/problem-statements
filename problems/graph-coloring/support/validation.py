import argparse
from parser import IOParser

def validateColoring(inputProblemPath, inputResultPath):
    inputGraph = IOParser.parse2nx(inputProblemPath)
    colors = IOParser.parse_solution(inputResultPath)

    for u, v in inputGraph.edges:
        if(colors[u] is None or colors[v] is None):
            return False

        if(colors[u] == colors[v]):
            return False

    return True


if __name__ == "__main__":  
    argParser = argparse.ArgumentParser()
    argParser.add_argument("inputProblem", type=str, help="Input file path of problem")
    argParser.add_argument("inputResult", type=str, help="Input file path of result")
    argParser.add_argument("output", type=str, help="Output file path")

    args = argParser.parse_args()

    is_valid = validateColoring(args.inputProblem, args.inputResult)
    if is_valid:
        with open(args.output, "w") as f:
            f.write("Valid coloring\n")
        print("Valid coloring")
    else:
        with open(args.output, "w") as f:
            f.write("Invalid coloring\n")
        print("Invalid coloring")
