#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2026 Alexandre D. Jesus <me@adbjesus.com>
#
# SPDX-License-Identifier: Apache-2.0

from collections import defaultdict

n = int(input())
dist = [(2*n+1) * [-1] for _ in range(2*n+1)]
dist[0][0] = 0
dist[0][1:n+1] = map(int, input().split())
dist[0][-1:-n-1:-1] = map(int, input().split())
for i, d in zip(range(1, n+1), map(int, input().split())):
    dist[i][0] = d
for i, d in zip(range(1, n+1), map(int, input().split())):
    dist[-i][0] = d
for i in range(1, n+1):
    dist[i][1:n+1] = map(int, input().split())
for i in range(1, n+1):
    dist[i][-1:-n-1:-1] = map(int, input().split())
for i in range(1, n+1):
    dist[-i][-1:-n-1:-1] = map(int, input().split())
for i in range(1, n+1):
    dist[-i][1:n+1] = map(int, input().split())

# Tests that if a -1 exists, it exists on all distance for that
# container/direction
inv = set()
for i in range(-n, n+1):
    if dist[0][i] == -1:
        inv.add(i)

assert 0 not in inv, inv
for i in range(-n, n+1):
    for j in range(-n, n+1):
        if i in inv or j in inv:
            assert dist[i][j] == -1, (i, j, dist[i][j])
        elif i == j:
            assert dist[i][j] == 0, (i, j, dist[i][j])
        else:
            assert dist[i][j] > 0, (i, j, dist[i][j])

# Tests triangle inequality.
for a in range(-n, n+1):
    for b in range(-n, n+1):
        if b == 0:
            continue
        for c in range(-n, n+1):
            ab = dist[a][b]
            bc = dist[b][c]
            ac = dist[a][c]
            if -1 in (ab, bc, ac):
                continue
            assert ac <= ab + bc, (a, b, c, ab, bc, ab+bc, ac)
