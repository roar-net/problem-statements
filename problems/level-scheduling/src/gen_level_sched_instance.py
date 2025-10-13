#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# SPDX-FileCopyrightText: © 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0

import random, math, sys

def poisson_variate(lmbda):
    """
    Inverse transform sampling method described in
    https://en.wikipedia.org/wiki/Poisson_distribution
    """
    x = 0
    s = p = math.exp(-lmbda)
    u = random.random()
    while u > s:
        x += 1
        p *= lmbda / x
        s = s + p
    return x

def instance(T, M, P, a_pm_bar, S, MSC, B):
    """Instance generation loosely based on https://doi.org/10.1080/00207540701725067"""
    # Model demand (no. of units fo each model to build)
    d = M * [1]
    for _ in range(M, T):
        d[random.randrange(M)] += 1
    assert(sum(d) == T)
    # Demand coefficient matrix (parts per model)
    # Poisson distributed (reference above uses Bernoulli)
    a = []
    for p in range(P):
        r = []
        for m in range(M):
            r.append(poisson_variate(a_pm_bar))
        a.append(r)
    # Material station assignment (Station where each part is used)
    A = list(range(1, S+1)) * int(P / S) + random.sample(range(1, S+1), P % S)
    random.shuffle(A)
    # Size of cargo carrier
    G = [random.randrange(2, MSC+1) for _ in range(P)]
    # Space constraint
    C = [ int(B * sum(G[p] for p in range(P) if A[p] == s)) for s in range(1, S+1)]
    return d, a, A, G, C

if __name__ == '__main__':
    if len(sys.argv) < 8:
        print("""Usage: {} T M P a S MSC B [seed]
where:
    T    - Total number of units to build
    M    - Number of models
    P    - Number of types of parts
    a    - Expected number of parts of each type in a model
    S    - Number of stations
    MSC  - Maximum size of cargo carrier
    B    - Tightness of storage space per station
    seed - Seed for the random number generator""".format(sys.argv[0]))
        exit()
    T, M, P = map(int, sys.argv[1:4])
    a_pm_bar = float(sys.argv[4])
    S, MSC = map(int, sys.argv[5:7])
    B = float(sys.argv[7])
    if len(sys.argv) >= 9:
        seed = int(sys.argv[8])
        random.seed(seed)
    invalid = True
    while invalid:
        d, a, A, G, C = instance(T, M, P, a_pm_bar, S, MSC, B)
        if a.count(M*[0]) != 0: # all parts must be used by some model
            continue
        # check that all models are different (at most one may use zero parts)
        transposed = []
        for m in range(M):
            row = []
            for p in range(P):
                row.append(a[p][m])
            transposed.append(row)
        invalid = False
        for i in range(1, M):
            for j in range(i):
                if transposed[i] == transposed[j]:
                    invalid = True
                    break
            if invalid:
                break
    # Checks passed, print instance
    print(M, P)     # no. models, no. parts
    print(*d)       # Model demand
    for l in a:     # Demand coefficient matrix
        print(*l)
    print(S)        # no. stations
    print(*C)       # Storage space at each station
    print(*G)       # Capacity of each cargo carrier
    print(*A)     # Station index (in range 1..S) where each part is used
    # For completeness (not used in the paper (?), but already supported in the models)
    print(*([1]*P)) # Storage space required by each unit of part p
    print(*([0]*P)) # Quantity of each part p initially at the station
                    # (less than the capacity of the respective cargo carrier)

