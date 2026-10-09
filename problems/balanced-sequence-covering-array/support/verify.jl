# SPDX-FileCopyrightText: 2026 Enrico Iurlano <eiurlano@tuwien.ac.at> and
#                              Luís Paquete <paquete@dei.uc.pt>
#
# SPDX-License-Identifier: CC-BY-4.0

#!/usr/bin/env julia
# BSCA reference verifier and evaluator.  No dependencies beyond the standard
# library, so it runs with a bare
#     julia verify.jl <instance.txt> <solution.txt>
#
# Exit status 0 if the solution is feasible; the objective value is printed.
# This is a port of support/verify.py and produces byte-identical output.

using Printf

"Non-empty, comment-stripped lines split on whitespace."
function fields(path)
    out = Vector{Vector{String}}()
    for raw in eachline(path)
        line = strip(first(split(raw, '#')))
        isempty(line) && continue
        push!(out, [String(p) for p in split(line)])
    end
    out
end

"One line: the number of events and the number of runs."
function read_instance(path)
    rec = fields(path)
    (isempty(rec) || length(rec[1]) < 2) &&
        error("instance must hold two integers, n and d")
    parse(Int, rec[1][1]), parse(Int, rec[1][2])
end

read_solution(path) = [[parse(Int, v) for v in row] for row in fields(path)]

"Ordered triples of distinct events that no run places in that order."
function uncovered(rows, n)
    pos = Vector{Vector{Int}}()
    for r in rows
        p = zeros(Int, n)
        for (j, e) in enumerate(r); p[e] = j; end
        push!(pos, p)
    end
    cnt = 0
    for a in 1:n, b in 1:n, c in 1:n
        (a == b || b == c || a == c) && continue
        any(p -> p[a] < p[b] < p[c], pos) || (cnt += 1)
    end
    cnt
end

"E = sum_{e,j} (C[e,j] - d/n)^2 = sum C^2 - d^2, an integer."
function imbalance(rows, n)
    d = length(rows)
    C = zeros(Int, n, n)
    for r in rows, (j, e) in enumerate(r); C[e, j] += 1; end
    sum(abs2, C) - d^2
end

function main(instpath, solpath)
    n, d = read_instance(instpath)
    rows = read_solution(solpath)

    errs = String[]
    length(rows) == d ||
        push!(errs, "solution has $(length(rows)) runs, instance requires $d")
    for (i, r) in enumerate(rows)
        sort(r) == collect(1:n) || push!(errs, "run $i is not a permutation of 1..$n")
    end
    if !isempty(errs)
        foreach(e -> println("INFEASIBLE: ", e), errs)
        return 1
    end

    u = uncovered(rows, n)
    if u != 0
        @printf("INFEASIBLE: %d of %d ordered triples uncovered\n", u, n*(n-1)*(n-2))
        return 1
    end

    E  = imbalance(rows, n)
    r  = mod(d, n)
    lo = r * (n - r)
    hi = d^2 * (n - 1)
    println("FEASIBLE")
    @printf("  instance      n = %d   d = %d\n", n, d)
    @printf("  runs          %d\n", length(rows))
    @printf("  imbalance     E = %d   attainable range: [%d, %d]\n", E, lo, hi)
    @printf("  objective     %d\n", E)
    return 0
end

length(ARGS) == 2 || (println("usage: julia verify.jl <instance.txt> <solution.txt>"); exit(2))
exit(main(ARGS[1], ARGS[2]))
