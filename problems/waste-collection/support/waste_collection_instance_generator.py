#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2026 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0

import sys
import random
from operator import itemgetter

if len(sys.argv) < 6:
    print(f"Usage: {sys.argv[0]} n owr dmin dmax seed")
    exit()

n = int(sys.argv[1])
owr = int(sys.argv[2])
dmin = int(sys.argv[3])
dmax = int(sys.argv[4])
seed = int(sys.argv[5])
random.seed(seed)

s = 0       # Source, aka depot
t = n+1     # Target, aka waste treatment plant

allnodes = range(s, t+1)
nodes = range(s+1, t)
dirs = (0, 1)

# Set up a purely random distance matrix
dist = []
for _ in dirs:
    aux1 = []
    for _ in dirs:
        aux2 = []
        for _ in allnodes:
            aux3 = []
            for _ in allnodes:
                aux3.append(random.randint(dmin, dmax))
            aux2.append(aux3)
        aux1.append(aux2)
    dist.append(aux1)

# From a node to itself in the same direction is 0 
for d in dirs:
    for i in allnodes:
        dist[d][d][i][i] = 0

# A node to itself in a different direction is not possible (represented as -1)
for d1 in dirs:
    for d2 in dirs:
        if d1 != d2:
            for i in allnodes:
                dist[d1][d2][i][i] = -1

# From every node to the source in any direction is impossible (represented as -1)
for d1 in dirs:
    for d2 in dirs:
        for i in allnodes:
            dist[d1][d2][i][s] = -1

# From the source to every node in direction other than 0 is impossible (represented as -1)
for d1 in dirs:
    if d1 != 0:
        for d2 in dirs:
            for i in allnodes:
                dist[d1][d2][s][i] = -1

# From the target to every node in any direction is impossible (represented as -1)
for d1 in dirs:
    for d2 in dirs:
        for i in allnodes:
            dist[d1][d2][t][i] = -1

# From every node to the target arriving in a direction other than 0 is impossible (represented as -1)
for d1 in dirs:
    for d2 in dirs:
        if d2 != 0:
            for i in allnodes:
                dist[d1][d2][i][t] = -1

# One-way roads
oneway = random.sample(nodes, owr//2)
otherway = random.sample(list(set(nodes)-set(oneway)), owr-owr//2)
for i in oneway:
    for d2 in dirs:
        for j in allnodes:
            dist[1][d2][i][j] = -1
            dist[d2][1][j][i] = -1
for i in otherway:
    for d2 in dirs:
        for j in allnodes:
            dist[0][d2][i][j] = -1
            dist[d2][0][j][i] = -1

# Enforce the triangular inequality (Floyd–Warshall's algorithm)
for d1 in dirs:
    for i1 in allnodes: # k
        for d2 in dirs:
            for i2 in allnodes: # i
                for d3 in dirs:
                    for i3 in allnodes: # j
                        dik = dist[d2][d1][i2][i1]
                        if dik == -1:
                            continue
                        dkj = dist[d1][d3][i1][i3]
                        if dkj == -1:
                            continue
                        dij = dist[d2][d3][i2][i3]
                        if dij == -1 or dik + dkj < dij:
                            dist[d2][d3][i2][i3] = dik + dkj

with open(f"random{n}_{owr}_{dmin}_{dmax}_{seed}.txt", "w") as f:
    f.write(f"{n}\n")
    # Print source
    f.write(' '.join(map(str, dist[0][0][s][s+1:t]))+'\n')
    f.write(' '.join(map(str, dist[0][1][s][s+1:t]))+'\n')
    # Print target
    f.write(' '.join(map(str, map(itemgetter(t), dist[0][0][s+1:t])))+'\n')
    f.write(' '.join(map(str, map(itemgetter(t), dist[1][0][s+1:t])))+'\n')
    # Print d00
    for i in nodes:
        f.write(' '.join(map(str, dist[0][0][i][s+1:t]))+'\n')
    # Print d01
    for i in nodes:
        f.write(' '.join(map(str, dist[0][1][i][s+1:t]))+'\n')
    # Print d11
    for i in nodes:
        f.write(' '.join(map(str, dist[1][1][i][s+1:t]))+'\n')
    # Print d10
    for i in nodes:
        f.write(' '.join(map(str, dist[1][0][i][s+1:t]))+'\n')
