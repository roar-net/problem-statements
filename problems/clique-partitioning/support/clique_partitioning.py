#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2025 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
# SPDX-FileCopyrightText: 2025 Andreia P. Guerreiro <andreia.guerreiro@tecnico.ulisboa.pt>
#
# SPDX-License-Identifier: Apache-2.0

import sys, random, math, time
from tabulate import tabulate

def sparse_fisher_yates_iter(n):
    """Sparse Fisher-Yates Sampler.
       See <https://doi.org/10.48550/arXiv.2104.05091>."""
    p = dict()
    for i in range(n-1, -1, -1):
        r = random.randrange(i+1)
        yield p.get(r, r)
        if i != r:
            # p[r] = p.pop(i, i) # saves memory, takes time
            p[r] = p.get(i, i) # lazy, but faster

def lcg_iter(n):
    "Pseudorandom sampling without replacement in O(1) space"
    if n > 0:
        a = 5 # always 5
        m = 1 << math.ceil(math.log2(n))
        if m > 1:
            c = random.randrange(1, m, 2)   # random odd number
            x = random.randrange(m)         # random starting value
            for _ in range(m):
                if x < n: yield x
                x = (a * x + c) % m
        else:
            yield 0


class AddMove:
    def __init__(self, neighbourhood, v, c):
        self.neighbourhood = neighbourhood
        self.v = v
        self.c = c

    def __str__(self):
        return f"Move: add vertex {self.v} to clique {self.c}"

    def _upper_bound_increment(self, solution):
        ub_incr = solution.incr_tab[self.v][-1]
        if self.c in solution.partition:
            ub_incr += solution.incr_tab[self.v][self.c]
        return ub_incr

    def lower_bound_increment(self, solution):
        assert self.v in solution.unassigned
        assert self.c in solution.partition or (len(solution.unused) == 0 and
            self.c == len(solution.partition)) or self.c == solution.unused[-1]
        return -self._upper_bound_increment(solution)

    def apply_move(self, solution):
        assert self.v in solution.unassigned
        assert self.c in solution.partition or (len(solution.unused) == 0 and
            self.c == len(solution.partition)) or self.c == solution.unused[-1]
        prob = solution.problem
        # Update solution evaluation
        solution.ub += self._upper_bound_increment(solution)
        # Update solution state, including ub increment pre-calculation
        solution.clique[self.v] = self.c
        solution.assigned.append(self.v)
        solution.unassigned.remove(self.v)
        partition = solution.partition
        if self.c not in partition:
            partition[self.c] = set()
            if len(solution.unused) == 0:
                for row in solution.incr_tab:
                    row.insert(self.c, 0)
            else:
                solution.unused.pop()
        for v in range(prob.sz):
            incr_row = solution.incr_tab[v]
            w = prob.mx[v][self.v]
            if w > 0:
                incr_row[-1] -= w
            incr_row[self.c] += w
        partition[self.c].add(self.v)
        return solution

    def revert_move(self, solution):
        #FIXME: This is virtually identical to RemoveMove.apply_move()
        assert self.v in solution.assigned
        assert self.v not in solution.unassigned
        assert self.v in solution.partition[self.c]
        assert solution.clique[self.v] == self.c
        prob = solution.problem
        # Update solution evaluation
        solution.ub -= solution.incr_tab[self.v][-1] + solution.incr_tab[self.v][self.c]
        # Update solution state, including ub increment pre-calculation
        solution.clique[self.v] = None
        solution.assigned.remove(self.v) # Linear time, but ok here
        solution.unassigned.add(self.v)
        partition = solution.partition
        for v in range(prob.sz):
            incr_row = solution.incr_tab[v]
            w = prob.mx[v][self.v]
            if w > 0:
                incr_row[-1] += w
            incr_row[self.c] -= w
        partition[self.c].remove(self.v)
        if len(partition[self.c]) == 0:
            solution.unused.append(self.c)
            del partition[self.c]
        return solution


class RemoveMove:
    def __init__(self, neighbourhood, v, c):
        self.neighbourhood = neighbourhood
        self.v = v
        self.c = c

    def __str__(self):
        return f"Move: remove vertex {self.v} from clique {self.c}"

    def _upper_bound_increment(self, solution):
        ub_incr = -solution.incr_tab[self.v][-1] - solution.incr_tab[self.v][self.c]
        return ub_incr

    def lower_bound_increment(self, solution):
        assert self.c == solution.clique[self.v]
        return -self._upper_bound_increment(solution)

    def apply_move(self, solution):
        assert self.v in solution.assigned
        assert self.v not in solution.unassigned
        assert self.v in solution.partition[self.c]
        assert solution.clique[self.v] == self.c
        prob = solution.problem
        # Update solution evaluation
        solution.ub += self._upper_bound_increment(solution)
        # Update solution state, including ub increment pre-calculation
        solution.clique[self.v] = None
        solution.assigned.remove(self.v) # Linear time, but ok here
        solution.unassigned.add(self.v)
        partition = solution.partition
        for v in range(prob.sz):
            incr_row = solution.incr_tab[v]
            w = prob.mx[v][self.v]
            if w > 0:
                incr_row[-1] += w
            incr_row[self.c] -= w
        partition[self.c].remove(self.v)
        if len(partition[self.c]) == 0:
            solution.unused.append(self.c)
            del partition[self.c]
        return solution


class ReallocMove:
    def __init__(self, neighbourhood, v, c0, c1):
        self.neighbourhood = neighbourhood
        self.v = v
        self.c0 = c0
        self.c1 = c1

    def __str__(self):
        return f"Move: move vertex {self.v} from clique {self.c0} to clique {self.c1}"

    def _upper_bound_increment(self, solution):
        ub_incr = -solution.incr_tab[self.v][self.c0]
        if self.c1 in solution.partition:
            ub_incr += solution.incr_tab[self.v][self.c1]
        return ub_incr

    def objective_value_increment(self, solution):
        assert self.c0 == solution.clique[self.v]
        assert self.c1 in solution.partition or (len(solution.unused) == 0 and
            self.c1 == len(solution.partition)) or self.c1 == solution.unused[-1]
        return -self._upper_bound_increment(solution)

    def apply_move(self, solution):
        assert self.v in solution.assigned
        assert self.v not in solution.unassigned
        assert self.v in solution.partition[self.c0]
        assert solution.clique[self.v] == self.c0
        assert self.c1 in solution.partition or (len(solution.unused) == 0 and
            self.c1 == len(solution.partition)) or self.c1 == solution.unused[-1]
        prob = solution.problem
        # Update solution evaluation
        solution.ub += self._upper_bound_increment(solution)
        # Update solution state, including ub increment pre-calculation
        solution.clique[self.v] = self.c1
        partition = solution.partition
        # Expand incr_tab if needed
        if self.c1 not in partition:
            partition[self.c1] = set()
            if len(solution.unused) == 0:
                for row in solution.incr_tab:
                    row.insert(self.c1, 0)
            else:
                solution.unused.pop()
        # Remove v from c0 and add to c1
        for v in range(prob.sz):
            incr_row = solution.incr_tab[v]
            incr_row[self.c0] -= prob.mx[v][self.v]
            incr_row[self.c1] += prob.mx[v][self.v]
        partition[self.c0].remove(self.v)
        partition[self.c1].add(self.v)
        # Remove partition c0 if empty
        if len(partition[self.c0]) == 0:
            solution.unused.append(self.c0)
            del partition[self.c0]
        return solution

    def revert_move(self, solution):
        inverse_move = ReallocMove(self.neighbourhood, self.v, self.c1, self.c0)
        return inverse_move.apply_move(solution)


class SwapMove:
    def __init__(self, neighbourhood, v0, v1):
        self.neighbourhood = neighbourhood
        self.v0 = v0
        self.v1 = v1

    def __str__(self):
        return f"Move: swap vertex {self.v0} in clique {self.c0} with vertex {self.v1} in clique {self.c1}"

    def _upper_bound_increment(self, solution):
        v0, v1 = self.v0, self.v1
        c0, c1 = solution.clique[v0], solution.clique[v1]
        # Move v0 from c0 to c1
        ub_incr = solution.incr_tab[v0][c1] - solution.incr_tab[v0][c0]
        # Move v1 from c1 to c0
        ub_incr += solution.incr_tab[v1][c0] - solution.incr_tab[v1][c1]
        # Correction
        ub_incr -= 2 * solution.problem.mx[v0][v1]
        return ub_incr

    def objective_value_increment(self, solution):
        assert solution.clique[self.v0] != solution.clique[self.v1]
        assert solution.clique[self.v0] in solution.partition
        assert solution.clique[self.v1] in solution.partition
        return -self._upper_bound_increment(solution)

    def apply_move(self, solution):
        prob = solution.problem
        clique = solution.clique
        partition = solution.partition
        v0, v1 = self.v0, self.v1
        c0, c1 = solution.clique[v0], solution.clique[v1]
        assert c0 != c1
        assert c0 in partition and c1 in partition
        assert v0 in partition[c0] and self.v1 in partition[c1]
        assert v0 in solution.assigned and v1 in solution.assigned
        assert v0 not in solution.unassigned and v1 not in solution.unassigned
        # Update solution evaluation
        solution.ub += self._upper_bound_increment(solution)
        # Update solution state, including ub increment pre-calculation
        clique[v0], clique[v1] = c1, c0
        # Remove v0 from c0 and add to c1, Remove v1 from c1 and add to c0
        for v in range(prob.sz):
            incr_row = solution.incr_tab[v]
            incr_row[c0] += prob.mx[v][v1] - prob.mx[v][v0]
            incr_row[c1] += prob.mx[v][v0] - prob.mx[v][v1]
        partition[c0].remove(v0)
        partition[c0].add(v1)
        partition[c1].remove(v1)
        partition[c1].add(v0)
        return solution

    def revert_move(self, solution):
        return self.apply_move(solution)


class Neighbourhood:
    def __init__(self, problem):
        self.problem = problem


class AddNextNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        if len(solution.unassigned):
            v = len(solution.assigned)
            assert v in solution.unassigned
            # Existing cliques
            for c in solution.partition.keys():
                yield AddMove(self, v, c)
            c = solution.unused[-1] if len(solution.unused) != 0 else len(solution.partition)
            yield AddMove(self, v, c)


class AddNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        for v in solution.unassigned:
            # Existing cliques
            for c in solution.partition.keys():
                yield AddMove(self, v, c)
            c = solution.unused[-1] if len(solution.unused) != 0 else len(solution.partition)
            yield AddMove(self, v, c)


class RemoveNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        for v in solution.assigned:
            yield RemoveMove(self, v, solution.clique[v])

    def random_move(self, solution):
        assert self.problem == solution.problem
        if len(solution.assigned):
            v = random.choice(solution.assigned)
            return RemoveMove(self, v, solution.clique[v])


# Move a vertex from one clique to another
class ReallocNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        if len(solution.unassigned) == 0:
            partition = solution.partition
            for v in range(self.problem.sz):
                c0 = solution.clique[v]
                for c1 in partition.keys():
                    if c1 != c0 and (len(partition[c0]) > 1 or len(partition[c1]) > 1 or max(partition[c1]) < v):
                        # NOTE: max(partition[c1]) is only called when both cliques
                        # have size 1. tuple(partition[c1])[0] could also be used.
                        # When joining two partitions of size 1, move the vertex
                        # with larger index into the partition of the other vertex
                        yield ReallocMove(self, v, c0, c1)
                if len(partition[c0]) > 2 or len(partition[c0]) == 2 and v == max(partition[c0]):
                    # NOTE: When spliting a partition of size 2 into two partitions of
                    # size 1, move the vertex with larger index into a new partition
                    c1 = solution.unused[-1] if len(solution.unused) != 0 else len(partition)
                    yield ReallocMove(self, v, c0, c1)

    def random_move(self, solution):
        assert self.problem == solution.problem
        if len(solution.unassigned) == 0:
            sz = self.problem.sz
            partition = solution.partition
            part_keys = tuple(partition.keys())    # FIXME: this takes linear time
            while True:
                x = random.randrange(sz * len(partition))
                v = x % sz
                c0 = solution.clique[v]
                c1 = part_keys[x // sz]
                if c1 != c0 and (len(partition[c0]) > 1 or len(partition[c1]) > 1 or max(partition[c1]) < v):
                    # NOTE: max(partition[c1]) is only called when both cliques
                    # have size 1. tuple(partition[c1])[0] could also be used.
                    return ReallocMove(self, v, c0, c1)
                elif c1 == c0 and len(partition[c0]) > 2 or len(partition[c0]) == 2 and v == max(partition[c0]):
                    c1 = solution.unused[-1] if len(solution.unused) != 0 else len(partition)
                    return ReallocMove(self, v, c0, c1)

    def random_moves_without_replacement(self, solution):
        assert self.problem == solution.problem
        if len(solution.unassigned) == 0:
            sz = self.problem.sz
            partition = solution.partition
            part_keys = tuple(partition.keys())    # FIXME: this takes linear time
            for x in lcg_iter(sz * len(partition)):
                v = x % sz
                c0 = solution.clique[v]
                c1 = part_keys[x // sz]
                if c1 != c0 and (len(partition[c0]) > 1 or len(partition[c1]) > 1 or max(partition[c1]) < v):
                    # NOTE: max(partition[c1]) is only called when both cliques
                    # have size 1. tuple(partition[c1])[0] could also be used.
                    yield ReallocMove(self, v, c0, c1)
                elif c1 == c0 and len(partition[c0]) > 2 or len(partition[c0]) == 2 and v == max(partition[c0]):
                    c1 = solution.unused[-1] if len(solution.unused) != 0 else len(partition)
                    yield ReallocMove(self, v, c0, c1)


# Swap two vertices from different cliques
class SwapNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        if len(solution.unassigned) == 0:
            partition = solution.partition
            c = tuple(partition.keys())
            for i in range(1, len(c)):
                ci = c[i]
                for vi in partition[ci]:
                    for j in range(i):
                        cj = c[j]
                        for vj in partition[cj]:
                            yield SwapMove(self, vi, vj)

    def random_move(self, solution):
        assert self.problem == solution.problem
        if len(solution.unassigned) == 0 and len(solution.partition) > 1:
            clique = solution.clique
            while True:
                vi, vj = random.sample(range(self.problem.sz), 2)
                ci, cj = clique[vi], clique[vj]
                if ci != cj:
                    return SwapMove(self, vi, vj)

    def random_moves_without_replacement(self, solution):
        assert self.problem == solution.problem
        if len(solution.unassigned) == 0 and len(solution.partition) > 1:
            clique = solution.clique
            sz = self.problem.sz
            for x in lcg_iter(sz*(sz-1)//2):
                vi = (1 + math.isqrt(1+8*x))//2
                vj = x - vi*(vi-1)//2
                ci, cj = clique[vi], clique[vj]
                if ci != cj:
                    yield SwapMove(self, vi, vj)


class LocalNeighbourhood(Neighbourhood):
    def __init__(self, problem):
        self.problem = problem
        self._realloc_nbhood = ReallocNeighbourhood(problem)
        self._swap_nbhood = SwapNeighbourhood(problem)

    def moves(self, solution):
        yield from self._realloc_nbhood.moves(solution)
        yield from self._swap_nbhood.moves(solution)

    # FIXME: Although this does not shuffle moves of the two types, it
    #        seems to perform well. When all moves are shuffled
    #        together, it appears that the first improving moves found
    #        are mostly Realloc moves. This should be investigated
    #        properly. It also raises the question of how random the
    #        move sequence should be meant to be.
    def random_moves_without_replacement(self, solution):
        yield from self._realloc_nbhood.random_moves_without_replacement(solution)
        yield from self._swap_nbhood.random_moves_without_replacement(solution)


class Solution:
    def __init__(self, problem, clique, partition, assigned, unassigned, unused, incr_tab, ub):
        self.problem = problem
        self.clique = clique
        self.partition = partition
        self.assigned = assigned
        self.unassigned = unassigned
        self.unused = unused
        self.incr_tab = incr_tab
        self.ub = ub

    def __str__(self):
        obj = 0
        for v in self.partition.values():
            v = tuple(v)
            for i in range(1, len(v)):
                for j in range(i):
                    obj += self.problem.mx[v[i]][v[j]]
        return f"Solution: partition = {self.partition}, unassigned = {self.unassigned}, unused = {self.unused}, #cliques = {len(self.partition)}, ub = {self.ub}, obj = {obj}"

    def copy_solution(self):
        return Solution(self.problem,
                        self.clique.copy(),
                        {k: clq.copy() for k, clq in self.partition.items()},
                        self.assigned.copy(),
                        self.unassigned.copy(),
                        self.unused.copy(),
                        [row.copy() for row in self.incr_tab],
                        self.ub)

    def objective_value(self):
        if len(self.unassigned) == 0:
            return -self.ub

    def lower_bound(self):
        return -self.ub

    def to_textio(self, f):
        if len(self.unassigned) == 0:
            f.write('\n'.join(sorted(map(' '.join, (map(str, sorted(clq)) for clq in self.partition.values())))))
            f.write('\n')


class Problem:
    def __init__(self, mx):
        self.mx = tuple(tuple(row for row in mx))
        self.c_neighbourhood = None
        self.d_neighbourhood = None
        self.l_neighbourhood = None
        self.p_neighbourhood = None
        self.sz = len(mx)
        self.ub = 0
        for i in range(self.sz):
            self.ub += sum(x for x in self.mx[i][i+1:] if x > 0)
        self.urn_pmf = self._urn_pmf(self.sz)

    def _urn_pmf(self, n):
        """
        _urn_pmf(n) returns a list of weights w[u] proportional to (u**n / u!).
        See eq. (1.4) in https://doi.org/10.1016/0097-3165(83)90009-2
        Used for random solution generation.
        """
        # Find the peak of the pmf
        j = n
        while ((j-1)/j)**n * j >= 1:
            j -= 1
        out = j * [0.0]
        out.append(1.)
        # Compute the values to the left (out[0] = 0)
        for k in range(j, 0, -1):
            out[k-1] = out[k] * ((k-1)/k)**n * k
        s = sum(out)
        # Compute the values to the right
        for k in range(j, 20*n):
            x = out[k] * ((k+1)/k)**n / (k+1)
            if s + x == s:
                break
            s += x
            out.append(x)
        return tuple(out)

    def __str__(self):
        return(f"Problem instance: mx =\n{tabulate(self.mx, tablefmt='plain')}\nub = {self.ub}")

    def construction_neighbourhood(self):
        if self.c_neighbourhood is None:
            self.c_neighbourhood = AddNeighbourhood(self)
        return self.c_neighbourhood

    def destruction_neighbourhood(self):
        if self.d_neighbourhood is None:
            self.d_neighbourhood = RemoveNeighbourhood(self)
        return self.d_neighbourhood

    def local_neighbourhood(self):
        if self.l_neighbourhood is None:
            self.l_neighbourhood = LocalNeighbourhood(self)
        return self.l_neighbourhood

    def perturbation_neighbourhood(self):
        if self.p_neighbourhood is None:
            self.p_neighbourhood = SwapNeighbourhood(self)
        return self.p_neighbourhood

    def empty_solution(self):
        unassigned = set(range(self.sz))
        incr_tab = [[0] for i in range(self.sz)]
        return Solution(self, self.sz*[None], {}, [], unassigned, [], incr_tab, self.ub)

    def random_solution(self):
        # To achieve uniform partition sampling, the urn model proposed in
        # https://doi.org/10.1016/0097-3165(83)90009-2 is used. The number of
        # urns, n_urns, is a random variate with pmf proportional to
        # (n_urns**n / n_urns!).
        n_urns = random.choices(range(len(self.urn_pmf)), weights=self.urn_pmf)[0]
        assignment = [random.randrange(n_urns) for _ in range(self.sz)]
        # canonicalise clique ids
        clique = []
        partition = {}
        mapping = {}
        k = 0
        for i in range(len(assignment)):
            c = mapping.setdefault(assignment[i], k)
            clique.append(c)
            partition.setdefault(c, set()).add(i)
            k = len(mapping)
        assigned = list(range(self.sz))
        # Compute objective value (same as upper bound)
        ub = 0
        for v in partition.values():
            v = tuple(v)
            for i in range(1, len(v)):
                for j in range(i):
                    ub += self.mx[v[i]][v[j]]
        # Initialize incr_tab
        incr_tab = []
        for v0 in range(self.sz):
            row = (k+1)*[0]
            for v1 in range(self.sz):
                w = self.mx[v0][v1]
                row[clique[v1]] += w
                if w > 0:
                    row[-1] -= w
            incr_tab.append(row)
        return Solution(self, clique, partition, assigned, set(), [], incr_tab, ub)

    @classmethod
    def from_textio(cls, f):
        L = map(int, f.read().split())
        n = next(L)
        mx = [ n*[0] for _ in range(n) ]
        for i in range(n):
            for j in range(i, n):
                # FIXME: Minus since reference instances are for minimisation
                mx[i][j] = mx[j][i] = -next(L)
        return cls(mx)

