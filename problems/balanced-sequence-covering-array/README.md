<!--
SPDX-FileCopyrightText: 2026 Enrico Iurlano <eiurlano@tuwien.ac.at> and
                        Luís Paquete <paquete@dei.uc.pt>

SPDX-License-Identifier: CC-BY-4.0
-->

# Balanced Sequence Covering Array Problem

Enrico Iurlano, Algorithms and Complexity Group, TU Wien, Austria

Luís Paquete, CISUC, University of Coimbra, Portugal

Copyright 2026 Enrico Iurlano, Luís Paquete.

This document is licensed under
[CC-BY-4.0](https://creativecommons.org/licenses/by/4.0/).

## Introduction

Many failures in event-driven systems are triggered not by *which* operations are performed but by the *order* in which they occur: a device is detached before it is released, a resource is written before it is locked, a stream is started before the codec is configured. Faults of this kind are invisible to a test suite that varies inputs but not orderings, and exhaustive order testing is hopeless already for a moderate number $n$ of events, since they admit $n!$ orderings.

The standard remedy is to cover all orderings of every *small* subset of events. A **strength-3 Sequence Covering Array** (SCA) on $n$ events (see [1, 3]) is a set of test runs, each run being a permutation of the $n$ events, such that for every ordered triple $(a,b,c)$ of distinct events at least one run contains $a$, then $b$, then $c$, not necessarily consecutively. Such an array exercises every order-dependent interaction among any three events, and remarkably few runs suffice: as Spencer showed [4], the number grows only logarithmically in $n$; see also [2] for an overview of the growth of comparable structures.

A suite can cover every triple and still be lopsided: an event may be scheduled first in nearly every run and last in none. This matters whenever the position of an event within a run carries cost or risk, such as setup time, operator attention or a warm-up effect, and it is generally undesirable for an event to be systematically favored. This problem fixes the number of runs at the size of the best published construction and asks for the most **positionally balanced** suite of that size.

## Task

Given a number of events $n$ and a number of runs $d$ (a priori known to be able to host a strength-3 SCA), find a strength-3 SCA on $n$ events using exactly $d$ runs that minimizes positional imbalance formalized in [Evaluation](#evaluation).

## Detailed description

### Parameters

An instance is a pair $(n, d)$ with $n \ge 4$ and $d \ge 1$ integers. Write $`[n] = \{1, \dots, n\}`$ for the set of events. The number of runs $d$ is **given**: it is the size of the best published strength-3 sequence covering array on $n$ events, so a feasible solution is known to exist, and it is not part of what is optimized.

### Solutions

A solution is a sequence $A = (A_1, \dots, A_d)$ of exactly $d$ runs, each run $A_i$ a permutation of $[n]$, written as a $d \times n$ array whose row $i$ is $A_i$. Write $`\mathrm{pos}_i(e)`$ for the position of event $e$ in run $i$, so that $`A_{i,\mathrm{pos}_i(e)} = e`$.

### Feasibility

$A$ **covers** an ordered triple $(a,b,c)$ of pairwise distinct events if some run places them in that relative order, i.e., if there is an $i$ with

$$\mathrm{pos}_i(a) < \mathrm{pos}_i(b) < \mathrm{pos}_i(c).$$

A solution is **feasible** if and only if it has exactly $d$ runs, every run is a permutation of $[n]$, and it covers all $n(n-1)(n-2)$ ordered triples of distinct events, i.e., if it is a strength-3 SCA of prescribed size $d$.

### Evaluation

Let $C_{ej}$ be the number of runs that place event $e$ in position $j$. Every row and every column of the $n \times n$ matrix $C$ sums to $d$, so a perfectly balanced suite is one with $C_{ej} = d/n$ for all $e, j$. The **objective**, to be minimized, is the sum-of-squares error from that ideal,

$$E(A)  =  \sum_{e=1}^{n}\sum_{j=1}^{n}(C_{ej} - \frac{d}{n})^2          =  \sum_{e=1}^{n}\sum_{j=1}^{n} C_{ej}^2  -  d^2,$$

always being a non-negative integer.

With
$r := (d \bmod n)$,

$$r(n-r)  \le  E(A)  \le  d^2(n-1).$$

The lower bound is attained by the cyclic array $A_{ij} = ((i + j - 2) \bmod n) + 1$, in which every event occupies every position as evenly as $d$ runs allow; it is zero exactly when $n$ divides $d$. The upper bound is attained by $d$ copies of a single permutation, where every event sits in one position in every run. A solver can therefore read $E(A)$ against the interval for the $d$ it is given and see at once how much of the available imbalance it has removed.

The cyclic array that attains the lower bound is in general not a strength-3 SCA, so the two criteria conflict, and the lower bound need not be attainable when insisting on full coverage.

Finally, the objective has a second reading that is often the more intuitive one. Write $d_H$ for the Hamming distance between two runs, i.e., the number of
positions in which they differ. Then

$$E(A)  =  d^2(n-1)  -  2 \sum_{1 \le i < k \le d} d_H(A_i, A_k),$$

so minimizing the imbalance is *exactly* maximizing how much the test runs differ from one another. A balanced suite is one whose runs are mutually as dissimilar as possible, and the upper bound above is the case in which no two runs differ at all.

### Instance data file

A single line holding two integers separated by whitespace: the number of events $n$ and the number of runs $d$. A `#` starts a comment and the rest of the line is ignored; blank lines are ignored.

### Solution file

One run per line: $n$ integers separated by whitespace, forming a permutation of $1, \dots, n$. Blank lines and `#` comments are ignored. The file must hold exactly $d$ runs.

### Example

#### Instance

`data/bsca-n04.txt`

```text
# BSCA instance, balanced sequence covering array: number of events, number of runs.
4 6
```

#### Solution

`data/bsca-example-solution-n04.txt`

```text
1 2 3 4
1 4 3 2
2 4 1 3
3 2 1 4
3 4 1 2
4 2 3 1
```

#### Explanation

The solution uses the prescribed $d = 6$ runs on $n = 4$ events. It is feasible: each of the $4 \cdot 3 \cdot 2 = 24$ ordered triples of distinct events appears in at least one run. For instance $(3,1,4)$ is covered by run 4, which is $3214$, since event 3 precedes event 1, which precedes event 4.

The count matrix $C$, with rows indexed by events and columns by positions, is

| event | pos 1 | pos 2 | pos 3 | pos 4 |
|-------|-------|-------|-------|-------|
| 1     | 2     | 0     | 3     | 1     |
| 2     | 1     | 3     | 0     | 2     |
| 3     | 2     | 0     | 3     | 1     |
| 4     | 1     | 3     | 0     | 2     |

every line of which sums to $d = 6$, as it must. A perfectly balanced suite would have every entry equal to $d/n = 1.5$, so the objective value is

$$E = \sum_{e,j}(C_{ej} - 1.5)^2 = 20.$$

At $d = 6$ and $n = 4$ we have $r = (6 \bmod 4) = 2$, so the imbalance of any suite of this size lies in $[r(n-r), d^2(n-1)] = [4, 108]$. This solution sits at $20$, well above the attainable minimum of $4$. Whether $4$ is attainable *together with* full coverage at $d = 6$ is exactly the kind of question this problem poses. Note also that events 1 and 3 have identical position profiles, as do events 2 and 4, and that no run places any event in position 2 except events 2 and 4. That is a visible symmetry which a more balanced solution would break.

The reference verifier is `support/verify.py` (Python 3); an equivalent Julia version is also available. It checks feasibility and reports the objective:

```text
$ python3 support/verify.py data/bsca-n04.txt data/bsca-example-solution-n04.txt
FEASIBLE
  instance      n = 4   d = 6
  runs          6
  imbalance     E = 20   attainable range: [4, 108]
  objective     20
```

### Instances

The `data` folder contains 33 instances, one for each event count

$$n = 4, 5, \dots, 30, 40, 50, 60, 70, 80, 90,$$

these being the counts tabulated for strength three by Torres-Jimenez et al. [5]. For each, $d$ is the size of the best-known construction from the same table. For $n \le 8$ that value is the proven optimum $d=N^{*}(n,3)$; for larger
$n$ the size $d$ is an upper bound, so for the instance a feasible strength-3 SCA exists.

## Acknowledgements

This problem statement is based on work from the COST Action Randomised Optimisation Algorithms Research Network (ROAR-NET), CA22137, supported by COST (European Cooperation in Science and Technology). It was prepared during a Short-Term Scientific Mission at CISUC, University of Coimbra.

## References

1. Y. M. Chee, C. J. Colbourn, D. Horsley, J. Zhou. *Sequence covering arrays.*
   SIAM Journal on Discrete Mathematics **27** (2013), 1844-1861.
   DOI: [10.1137/120894099](https://doi.org/10.1137/120894099)
1. E. Iurlano. *Growth of the perfect sequence covering array number.* Designs,
   Codes and Cryptography **91** (2023), 1487-1494.
   DOI: [10.1007/s10623-022-01168-3](https://doi.org/10.1007/s10623-022-01168-3)
1. D. R. Kuhn, J. M. Higdon, J. Lawrence, R. Kacker, Y. Lei. *Combinatorial
   methods for event sequence testing.* Fifth IEEE International Conference on
   Software Testing, Verification and Validation (ICST 2012), IEEE Computer
   Society, 2012, pp. 601-609.
   DOI: [10.1109/ICST.2012.147](https://doi.org/10.1109/ICST.2012.147)
1. J. Spencer. *Minimal scrambling sets of simple orders.* Acta Mathematica
   Academiae Scientiarum Hungaricae **22** (1971), 349-353.
   DOI: [10.1007/BF01896428](https://doi.org/10.1007/BF01896428)
1. J. Torres-Jimenez, D. O. Ramirez-Acuna, B. Acevedo-Juárez, H. Avila-George.
   *New upper bounds for sequence covering arrays using a 3-stage approach.*
   Expert Systems with Applications **207** (2022), 118022.
   DOI: [10.1016/j.eswa.2022.118022](https://doi.org/10.1016/j.eswa.2022.118022)
