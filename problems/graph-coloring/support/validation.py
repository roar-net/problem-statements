import argparse

def validate_coloring(input_path, output_path):
    
    return False

if __name__ == "__main__":  
    parser = argparse.ArgumentParser()
    parser.add_argument("inputProblem", type=str, help="Input file path of problem")
    parser.add_argument("inputResult", type=str, help="Input file path of result")
    parser.add_argument("output", type=str, help="Output file path")

    args = parser.parse_args()

    is_valid = validate_coloring(args.input, args.output)
    if is_valid:
        print("Valid coloring")
    else:
        print("Invalid coloring")
