#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-FileCopyrightText: © 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0

import sys

def read_instance(f):
    # Number of models and number of types of parts
    M, P = map(int, f.readline().split())
    assert M > 0
    assert P > 0
    # Model demand (no. of units fo each model to build)
    d = tuple(map(int, f.readline().split()))
    assert len(d) == M
    assert all(x > 0 for x in d)
    # Demand coefficient matrix (parts per model)
    a = []
    for _ in range(P):
        a.append(tuple(map(int, f.readline().split())))
        assert len(a[-1]) == M
        assert all(x >= 0 for x in a[-1])
    a = tuple(a)
    assert len(a) == P
    # Storage constraint information
    # Number of stations
    S = int(f.readline())
    assert 1 <= S <= P
    # Storage space available at each station
    C = tuple(map(int, f.readline().split()))
    assert len(C) == S
    assert all(x > 0 for x in C)
    # Capacity of cargo carrier for each part p
    G = tuple(map(int, f.readline().split()))
    assert len(G) == P
    assert all(x > 0 for x in G)
    # Station-part assignment
    A = tuple(map(int, f.readline().split()))
    assert len(A) == P
    assert all(1 <= x <= S for x in A)
    assert len(set(A)) == S
    # Storage space required by each unit of part p
    c = tuple(map(int, f.readline().split()))
    assert len(c) == P
    assert all(x > 0 for x in c)
    # Quantity of each part p initially stored in stock
    # (must be less than the capacity of the respective cargo carrier)
    L = tuple(map(int, f.readline().split()))
    assert len(L) == P
    assert all(map(lambda x, y: 0 <= x < y, L, G))
    return d, a, S, C, G, A, c, L

def read_solution(f, d):
    u = tuple(map(int, f.read().split()))
    M = len(d)
    T = sum(d)
    assert len(u) == T
    count = M * [0]
    for m in u:
        assert 1 <= m <= M
        count[m-1] += 1
    assert tuple(count) == d
    return u

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} instance_file solution_file".format(sys.argv[0]))
        exit()
    with open(sys.argv[1]) as fi:
        d, a, S, C, G, A, c, L = read_instance(fi)
    with open(sys.argv[2]) as fs:
        u = read_solution(fs, d)
    # Evaluate solution
    M = len(d)
    P = len(a)
    T = sum(d)
    # average part demand
    r = tuple([sum(map(lambda x, y: x*y, d, ap)) / T for ap in a])
    # part-demand deviation from average demand
    b = tuple([tuple([r[p] - a[p][m] for m in range(M)]) for p in range(P)])
    dev =  P * [0]
    J = 0
    for t in range(T):
        for p in range(P):
            dev[p] += b[p][u[t]-1]
            J += dev[p]**2
    # Storage
    L = list(L)
    l_max = S * [0]
    for p in range(P):
        l_max[A[p]-1] += c[p] * L[p]
    for t in range(T):
        l = S * [0]
        for p in range(P):
            L[p] = (L[p] - a[p][u[t]-1]) % G[p] # Always positive!
            l[A[p]-1] += c[p] * L[p]
        for s in range(S):
            if l_max[s] < l[s]:
                l_max[s] = l[s]
    print("J = %f," % J, "maximum storage =", tuple(l_max))
    for s in range(S):
        if l_max[s] > C[s]:
            print("Warning: Storage capacity ({}) exceeded at station {}".format(C[s], s+1))

