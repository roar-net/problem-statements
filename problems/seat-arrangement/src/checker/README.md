# Checker for the Seating Arrangement Problem

This checker validates solutions for the seating arrangement problem. If the solution is infeasible then an error is raised. If the solution is feasible then it the corresponding objective value is printed.

Run the checker with the following command:
```
python checker.py problem_instance_file solution_file
```

## Example

Run the checker to validate the solution in file `examples/solution1.out` for the problem instance in file `examples/example_weighted.in`:
```
python checker.py examples/example_weighted.in examples/solution1.out
```
The value 24 will be printed.

Run the checker to validate the solution in file `examples/solution1.out` for the problem instance in file `examples/example_weighted_with_disagreements.in`:
```
python checker.py examples/example_weighted_with_disagreements.in examples/solution1.out
```
An error will be raised.
