<!--
SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
SPDX-FileCopyrightText: 2025 Alexandre D. Jesus <me@adbjesus.com>

SPDX-License-Identifier: CC-BY-4.0
-->

# Level Scheduling

Carlos M. Fonseca, University of Coimbra, CISUC/LASI, DEI, Portugal  
Alexandre D. Jesus, A.P. Moller - Maersk, Portugal

Copyright 2025 Carlos M. Fonseca and Alexandre D. Jesus

This document is licensed under CC-BY-4.0.

## Introduction

Different models of a given product are manufactured in a mixed-model assembly
line, whereby different parts are assembled onto a base configuration of the
product at designated stations. Level scheduling consists in sequencing the
assembly of the different models required to meet the demand in such a way
that the rate of consumption of each type of part throughout the planning
horizon is close to constant. This is also known as the Output Rate
Variation (ORV) problem or the Monden problem (Bautista _et al._, 1996).

However, when parts of each type are supplied to stations in multiple-unit
cargo carriers and the storage space at each station is limited, nearly
constant part-consumption rates may lead to the violation of such storage
constraints due to the accummulation of multiple parts of different types at
the stations (Boysen _et al._, 2009).

## Task

The problem consists in determining the order in which given numbers of units
of the different models of a base product should be assembled to achieve a
smooth flow of parts to the corresponding stations while not exceeding the
part-storage capacity at each station.

## Detailed description

For a given base product, there is a number, $M$, of different models.
Assembling one unit of a given model requires certain numbers of parts of up
to $P$ types. Model units are assembled in a mixed-model assembly line
consisting of $S$ assembly stations, $1\leq S\leq P$, and it is assumed that
each type of part $p$ is used only at a given station $A_p$, $1\leq A_p\leq
S$. At the beginning of each day, the number of units, $d_m$, of each model
$m$, $1 \leq m \leq M$, to be assembled is defined. Thus, the total number of
units to be assembled in that line is $T = \sum_{m=1}^{M} d_m$. Model units
are assembled in sequence, requiring one time slot each. Since $T$ model units
are to be assembled in one day, there are also $T$ time slots.

In order to ensure a smooth flow of parts to the corresponding stations and
reduce part safety stock levels, it is desired that the rate of consumption of
the different parts throughout the day is kept as close to constant as
possible. In other words, the number of parts of type $p$, $1 \leq p \leq P$,
used up to slot $t$, $1 \leq t \leq T$, should be close to $t\cdot r_p$, where
$r_p$ is the total number of parts of type $p$ required to build all $d_m$
units of all models $m$, $1 \leq m \leq M$, divided by $T$.

A solution is a vector $u = (u_1, u_2, \dots, u_T)$ such that $1\leq u_t\leq
M$ and $\sum_{t=1}^{T} [u_t = m] = d_m$ for all $1\leq m\leq M$, where $u_t$
denotes the model to be assembled in time slot $t$ and $[u_t = m]$ denotes the
value $1$ if $u_t = m$ and $0$ otherwise. 

The cost of a solution $u$, to be minimised, is the sum of the squared
deviations between the target demand and the cumulated actual demand for all
part types and time slots. Mathematically:

$$J(u) = \sum_{t=1}^{T} \sum_{p = 1}^{P} \left(t\cdot r_p - \sum_{i=1}^{t} a_{p,u_i} \right)^2 $$

where $a_{p,u_i}$ denotes the number of parts type $p$ required by model $u_i$.

For each station, the storage space required by a given solution is the
maximum amount of space occupied by the parts in stock at that station
throughout the planning horizon. It is assumed that a new cargo carrier is
issued to a station only when the number of parts of that type
is lower than the number of parts required to assemble the current model.
Parts in a cargo carrier that are not used immediately remain at the station
and take the corresponding amount of space until they are used. Mathematically,
the maximum storage used at station $s$, $1\leq s\leq S$, is given by:

```math
\ell_{\max,s}(u) = \max_{t\in\{0,\dots,T\}} \left(\sum_{\substack{p = 1\\A_p=s}}^{P}
c_p\cdot\left[\left(L_p + t\cdot G_p - \sum_{i=1}^{t} a_{p,u_i} \right) \mod G_p \right]\right)
```

where $G_p$ denotes the number of parts of type $p$ in a cargo carrier, $L_p$
denotes the number of parts of type $p$ initially in stock at the station, and
$c_p$ denotes the space occupied by one part of type $p$. It follows from the
above restocking strategy that $L_p < G_p$ for all $p \in \lbrace 1,\dots, P\rbrace$.

A feasible solution must not require more storage space than the space, $C_s$,
available at each station $s$. Formally, $\ell_{\max,s}(u) < C_s$ for all $s
\in \lbrace 1,...,S\rbrace$.

## Instance data file

The first line of the input contains two space-separated integers, $M$ and
$P$, where $M$ is the number of different models to be assembled, and $P$ is
the number of different types of parts to be used.

The second line contains $M$ space-separated integers, $d_1, d_2, \dots, d_M$,
corresponding to the number of units of each model to assemble. 

The following $P$ lines give a space-separated matrix of the number of parts
of each type that are used in each model:

$$
\begin{array}{ccccc}
a_{1,1} & a_{1,2} & a_{1,3} & \dots & a_{1,M}\\
a_{2,1} & a_{2,2} & a_{2,3} & \dots & a_{2,M}\\
a_{3,1} & a_{3,2} & a_{3,3} & \dots & a_{3,M}\\
\vdots & \vdots & \vdots & \ddots & \vdots \\
a_{P,1} & a_{P,2} & a_{P,3} & \dots & a_{P,M}
\end{array}
$$

where $a_{p,m}$, $1 \leq p \leq P$ and $1 \leq m \leq M$, denotes the number
of parts of type $p$ needed to assemble one unit of model $m$.

The next line contains a single integer, $S$, denoting the number of stations.
It is followed by a line containing $S$ space-separated integers, $C_1, \dots,
C_S$, specifying the amount of storage space available at each station.

The last four lines of the input all contain $P$ space-separated integers
specifying, respectively:

- The capacity of cargo carriers for each type of part, $G_1, \dots, G_P$.
- The station in which each type of part is assembled, $A_1, \dots, A_P$.
- The storage space used by each type of part, $c_1, \dots, c_P$.
- The number of parts of each type initially available at the corresponding station, $L_1, \dots, L_P$.

## Solution file

A solution file lists the model indices $u_1, u_2, \dots, u_T$ in the order in
which the $T$ model units are to be assembled, one value per line.

## Example

### Instance

```
4 5
2 2 2 4
1 1 0 0
0 0 0 1
1 0 0 0
2 1 0 0
1 1 1 0
2
4 4
2 2 3 3 2
1 1 1 2 2
1 1 1 1 1
0 0 0 0 0
```

### Solution

```
3
2
4
1
4
3
2
4
1
4
```

$J(u) = 9.6000,\ \ell_{\max, 1}(u) = 4,\ \ell_{\max, 2}(u) = 3$

### Explanation

There are $M=4$ models and $P=5$ types of parts. Two units of each model 1, 2, and 3,
and four units of model 4 are to be assembled. Model 1 requires one part of
each type 1, 3 and 5, and two parts of type 4. Model 2 requires one part of
each type 1, 4 and 5. Models 3 and 4 require a single part of type 5 and 2,
respectively.

There are two stations in the assembly line, each with 4 units of storage
capacity. The number of parts in each cargo carrier is two for part types 1,
2, and 5, and three for part types 3 and 4. Parts of types 1, 2 and 3 are
assembled in station 1, and the remaining parts are assembled in station 2.
All parts require one unit of storage space, and no parts are assumed to be
available at the stations before assembly starts.

The solution indicates the order in which the two units of each
model 1, 2, and 3, and the four units of model 4 are to be assembled. 

## Acknowledgement

This problem statement is based upon work from COST Action Randomised
Optimisation Algorithms Research Network (ROAR-NET), CA22137, is supported by
COST (European Cooperation in Science and Technology).

## References

J. Bautista, R. Companys, and A. Corominas (1996). "Heuristics and exact
algorithms for solving the Monden problem," *European Journal of Operational
Research*, 88(1), 101-113.
\[ [DOI](https://doi.org/10.1016/0377-2217(94)00165-0) \]

N. Boysen, M. Fliedner, and Armin Schol (2009). "Level scheduling of mixed-model
assembly lines under storage constraints," *International Journal of
Production Research*, 47(10), 2669-2684.
\[ [DOI](https://doi.org/10.1080/00207540701725067) \]


