# SPDX-FileCopyrightText: 2025 Andreia P. Guerreiro <andreia.guerreiro@tecnico.ulisboa.pt>
#
# SPDX-License-Identifier: Apache-2.0

import sys
import numpy as np


def next_uncommented_line(f, start_comment="#"):
    line = f.readline()
    while line.strip().startswith(start_comment):
        line = f.readline()
    return line

def read_instance(fname):
    with open(fname, "r") as f:
        line = next_uncommented_line(f)
        G, T, L, d, l, u = list(map(int, line.split()))
        line = next_uncommented_line(f)
        W = np.array(list(map(int, line.split())), dtype=int)
        GL = []
        D = []
        for g in range(G):
            line = next_uncommented_line(f)
            GL.append(list(map(int, line.split())))
        for di in range(d):
            line = next_uncommented_line(f)
            D.append(list(map(int, line.split())))
    return GL, T, L, W, D, l, u

def read_solution(fname):
        x = np.loadtxt(fname, dtype=int)
        return x

def check(instance, sol):
    GL, T, L, W, D, l, u = instance
    G = len(GL)
    _, count = np.unique(sol, return_counts=True)
    assert len(sol) == G, f"There has to be {G} guests"
    assert (sol >= 0).all(), f"Invalid table assignment (negative index)"
    assert (sol < T).all(), f"Invalid table assignment (index greater than T-1)"
    assert (count >= l).all(), f"All tables must have at least {l} guests"
    assert (count <= u).all(), f"All tables must have at most {u} guests"

    for d in D:
        assert sol[d[0]] != sol[d[1]], f"Guests {d[0]} and {d[1]} cannot sit in the same table"

    TL = np.zeros((T, L), dtype=int)
    for g in range(G):
        t = sol[g]
        labels = GL[g]
        TL[t, labels] = 1
    return (TL*W[np.newaxis,:]).sum()

if __name__ == "__main__":
    instanceFile = sys.argv[1]
    solutionFile = sys.argv[2]

    instance = read_instance(instanceFile)
    solution = read_solution(solutionFile)
    obj = check(instance, solution)
    print(obj)
