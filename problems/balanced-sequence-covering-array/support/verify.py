# SPDX-FileCopyrightText: 2026 Enrico Iurlano <eiurlano@tuwien.ac.at> and
#                              Luís Paquete <paquete@dei.uc.pt>
#
# SPDX-License-Identifier: CC-BY-4.0

#!/usr/bin/env python3
"""BSCA reference verifier and evaluator.

Standard library only, so it runs with a bare
    python3 verify.py <instance.txt> <solution.txt>

Exit status 0 if the solution is feasible; the objective value is printed.
support/verify.jl is a Julia port and produces byte-identical output.
"""
import sys


def fields(path):
    """Non-empty, comment-stripped lines split on whitespace."""
    out = []
    with open(path, encoding="utf-8") as f:
        for raw in f:
            line = raw.split("#", 1)[0].strip()
            if not line:
                continue
            out.append(line.split())
    return out


def read_instance(path):
    """One line: the number of events and the number of runs."""
    rec = fields(path)
    if not rec or len(rec[0]) < 2:
        raise ValueError("instance must hold two integers, n and d")
    return int(rec[0][0]), int(rec[0][1])


def read_solution(path):
    return [[int(v) for v in row] for row in fields(path)]


def uncovered(rows, n):
    """Ordered triples of distinct events that no run places in that order."""
    pos = []
    for r in rows:
        p = [0] * (n + 1)
        for j, e in enumerate(r):
            p[e] = j
        pos.append(p)
    cnt = 0
    for a in range(1, n + 1):
        for b in range(1, n + 1):
            for c in range(1, n + 1):
                if a == b or b == c or a == c:
                    continue
                if not any(p[a] < p[b] < p[c] for p in pos):
                    cnt += 1
    return cnt


def imbalance(rows, n):
    """E = sum_{e,j} (C[e,j] - d/n)^2 = sum C^2 - d^2, an integer."""
    d = len(rows)
    C = [[0] * n for _ in range(n)]
    for r in rows:
        for j, e in enumerate(r):
            C[e - 1][j] += 1
    return sum(x * x for row in C for x in row) - d * d


def main(instpath, solpath):
    n, d = read_instance(instpath)
    rows = read_solution(solpath)

    errs = []
    if len(rows) != d:
        errs.append("solution has %d runs, instance requires %d" % (len(rows), d))
    for i, r in enumerate(rows, start=1):
        if sorted(r) != list(range(1, n + 1)):
            errs.append("run %d is not a permutation of 1..%d" % (i, n))
    if errs:
        for e in errs:
            print("INFEASIBLE: " + e)
        return 1

    u = uncovered(rows, n)
    if u != 0:
        print("INFEASIBLE: %d of %d ordered triples uncovered"
              % (u, n * (n - 1) * (n - 2)))
        return 1

    E = imbalance(rows, n)
    r = d % n
    lo = r * (n - r)
    hi = d * d * (n - 1)
    print("FEASIBLE")
    print("  instance      n = %d   d = %d" % (n, d))
    print("  runs          %d" % len(rows))
    print("  imbalance     E = %d   attainable range: [%d, %d]" % (E, lo, hi))
    print("  objective     %d" % E)
    return 0


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: python3 verify.py <instance.txt> <solution.txt>")
        sys.exit(2)
    sys.exit(main(sys.argv[1], sys.argv[2]))
