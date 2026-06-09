<!--
SPDX-FileCopyrightText: 2026 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
SPDX-FileCopyrightText: 2026 Alexandre D. Jesus <me@adbjesus.com>

SPDX-License-Identifier: CC-BY-4.0
-->

# Urban Waste Collection

Carlos M. Fonseca, University of Coimbra, CISUC/LASI, DEI, Portugal  
Alexandre D. Jesus, A.P. Moller - Maersk, Portugal

Copyright 2026 Alexandre Jesus, Carlos M. Fonseca.

This document is licensed under CC-BY-4.0.

## Introduction

In many cities, waste collection vehicles are used to regularly empty
public waste containers located on the side of roads. A given city
quarter is served by a single vehicle that is large enough to collect
the waste from all containers in a single tour. A collection tour
consists in the vehicle leaving the depot, visiting and emptying all
containers in the quarter, disposing of the collected waste at the
city's waste treatment plant, and returning to the depot.

On one-way and most two-way roads, the vehicle may empty the containers
it passes by regardless of whether or not it is driving on the side of
the road where the container is located. On multi-lane roads, however,
the vehicle and the container must be on the same side of the road for
the collection to be possible. In any case, no U-turns are allowed at
waste containers.

## Task

Determine the shortest tour for a waste collection vehicle that visits
all containers, starting at the depot and returning to it after
disposing of the collected waste at the waste treatment plant.

## Detailed description

An instance of the urban waste collection problem is defined by:

- The number of containers to visit, $N$
- The distances from the depot to each container for the two possible
  arrival directions (0 and 1)
- The distances from each container to the waste treatment plant for the
  two possible departing directions (0 and 1)
- Four $N \times N$ distance matrices, one for each combination of
  departing and arriving directions between containers (0-0, 0-1, 1-1,
  and 1-0)

A solution is a sequence of all $N$ containers to visit and the
corresponding directions.

Since U-turns are not permitted at container locations, a vehicle
arriving at a container in one direction must depart in the same
direction. The cost of a solution is the total distance travelled by the
vehicle. This includes the distance from the depot to the first
container, the sum of distances between all subsequent containers, and
the distance from the last container to the treatment plant, taking the
directions into account. The constant distance between the treatment
plant and the depot can be ignored for the purpose of optimisation. The
objective is to minimise the total distance travelled.

## Instance data file

The first line of the input contains a single integer, $N$, denoting the
number of containers to visit. The rest of the input consists of $4 +
4N$ additional lines, each containing $N$ integers separated by
whitespace (spaces or tabs).

The first of those lines contains the distances from the depot to each
container, arriving to the container in direction 0. The next line
contains the distances from the depot to each container, but arriving to
the container in direction 1. Similarly, the following two lines contain
the distances from each container to the treatment plant departing in
directions 0 and 1, respectively.

The next four sequences of $N$ lines are distance matrices for the $N$
containers, for each combination of directions. The value at position
$(r, c) \in \lbrace 1,\dots, N\rbrace^2$ of the first matrix is the
distance from container $r$ to container $c$ when departing from $r$ in
direction 0 and arriving at $c$ also in direction 0. The other three
matrices are analogous, corresponding to directions 0–1, 1–1 and
1–0, respectively. If a given direction at a container is not
permitted, all distances to and from that container in that direction
take the value -1.

## Solution file

The solution should be printed on consecutive lines, with the indices of
the $N$ containers and the corresponding directions in the order in
which they should be visited. Each line must contain a container index,
in $\lbrace 1, \dots, N\rbrace$, and the corresponding direction
(0 or 1) separated by whitespace.

## Example

### Instance

```text
3
60 26 -1
17 15 16
107 109 -1
40 138 87
0 130 -1
34 0 -1
-1 -1 -1
296 107 185
195 141 145
-1 -1 -1
0 180 54
189 0 198
122 179 0
193 195 -1
95 225 -1
139 181 -1
```

### Solution

```text
3 1
1 0
2 0
```

This solution has a total cost of 394.

### Explanation

There are $N=3$ containers to visit. Containers 1 and 2 can be emptied
when the vehicle passes by in either direction, but container 3
can only be emptied when passing by in direction 1 as indicated by the
-1 distance values.

The solution specifies that the vehicle starts at the depot and arrives
to container 3 in direction 1, travelling a distance of 16 (last value
in the third line of the instance data file). Then, the vehicle travels
a distance of 139 (first value in the last line) from container 3 in
direction 1 to container 1 in direction 0. Travelling from container 1
in direction 0 to container 2 in direction 0 costs a distance of 130
(second value in the sixth line). Finally, departing from this container
in direction 0 to the waste-treatment plant has cost 109 (second value
in the fourth line line). Therefore, the total cost is $16 + 139 + 130 +
109 = 394$.

