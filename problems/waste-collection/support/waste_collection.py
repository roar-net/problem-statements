#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: 2026 Carlos M. Fonseca <cmfonsec@dei.uc.pt>
#
# SPDX-License-Identifier: Apache-2.0

import math, sys, random, time
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

# ----------------------------------- Moves -----------------------------------

class InsertMove:
    def __init__(self, neighbourhood, i, k):
        self.neighbourhood = neighbourhood
        # i is an integer position in the current route
        # abs(k) is a waste container, sign denotes travel direction
        self.i = i
        self.k = k

    def __str__(self):
        return f"Insert move: {self.i}, {self.k}"

    def apply_move(self, solution):
        prob = solution.problem
        # Update lower bound
        prv = solution.tour[self.i-1]
        nxt = solution.tour[self.i]
        solution.lb += prob.dist[prv][self.k] + prob.dist[self.k][nxt] - prob.dist[prv][nxt]
        # Update tour
        # Using list.insert() may cost linear time, but this should still
        # be acceptable in apply_move().
        solution.tour.insert(self.i, self.k)
        solution.not_visited.remove(abs(self.k))
        return solution

    def lower_bound_increment(self, solution):
        prob = solution.problem
        prv = solution.tour[self.i-1]
        nxt = solution.tour[self.i]
        incr = prob.dist[prv][self.k] + prob.dist[self.k][nxt] - prob.dist[prv][nxt]
        return incr

class RemoveMove:
    def __init__(self, neighbourhood, i, k):
        self.neighbourhood = neighbourhood
        # i is an integer position in the current route
        # abs(k) is a waste container, sign denotes travel direction
        self.i = i
        self.k = k

    def __str__(self):
        return f"Remove move: {self.i}, {self.k}"

    def apply_move(self, solution):
        assert solution.tour[self.i] == self.k
        prob = solution.problem
        # Update lower bound
        prv = solution.tour[self.i-1]
        nxt = solution.tour[self.i+1]
        assert prob.dist[prv][nxt] != -1
        solution.lb += prob.dist[prv][nxt] - prob.dist[prv][self.k] - prob.dist[self.k][nxt]
        # Update tour
        solution.tour.pop(self.i)
        solution.not_visited.add(abs(self.k))
        return solution

    def lower_bound_increment(self, solution):
        assert solution.tour[self.i] == self.k
        prob = solution.problem
        prv = solution.tour[self.i-1]
        nxt = solution.tour[self.i+1]
        assert prob.dist[prv][nxt] != -1
        incr = prob.dist[prv][nxt] - prob.dist[prv][self.k] - prob.dist[self.k][nxt]
        return incr

class ReinsertionMove:
    def __init__(self, neighbourhood, i, j, s):
        self.neighbourhood = neighbourhood
        # i and j are integer positions in the current route
        # s indicates whether the sign changes
        self.i = i
        self.j = j
        self.s = s

    def __str__(self):
        return f"Reinsertion move: {self.i}, {self.j}, {self.s}"

    def apply_move(self, solution):
        prob = solution.problem
        # Update lower bound (really the objective value)
        solution.lb += self.objective_value_increment(solution)
        # Update tour
        i, j = self.i, self.j
        k = solution.tour[i]
        if j < i:
            solution.tour[j+1:i+1] = solution.tour[j:i]
        elif j > i:
            solution.tour[i:j] = solution.tour[i+1:j+1]
        solution.tour[j] = self.s * k
        return solution

    def objective_value_increment(self, solution):
        prob = solution.problem
        i, j = self.i, self.j
        # Remove bin in position i
        prv = solution.tour[self.i-1]
        k = solution.tour[self.i]
        nxt = solution.tour[self.i+1]
        incr = -prob.dist[prv][k] - prob.dist[k][nxt]
        # Insert at position j
        k *= self.s
        if j < i:
            incr += prob.dist[prv][nxt]
            prv = solution.tour[self.j-1]
            nxt = solution.tour[self.j]
            incr -= prob.dist[prv][nxt]
        elif j > i:
            incr += prob.dist[prv][nxt]
            prv = solution.tour[self.j]
            nxt = solution.tour[self.j+1]
            incr -= prob.dist[prv][nxt]
        incr += prob.dist[prv][k] + prob.dist[k][nxt]
        return incr


class ThreeOptMove:
    def __init__(self, neighbourhood, i, j, k):
        self.neighbourhood = neighbourhood
        self.i = i
        self.j = j
        self.k = k

    def __str__(self):
        return f"3-Opt move: {self.i}, {self.j}, {self.k}"

    def apply_move(self, solution):
        prob = solution.problem
        # Update lower bound (really the objective value)
        solution.lb += self.objective_value_increment(solution)
        # Update tour
        i, j, k = self.i, self.j, self.k
        # Must replace the last slice first
        temp = solution.tour[j:k]
        solution.tour[j:k] = solution.tour[i:j]
        solution.tour[i:j] = temp
        return solution

    def objective_value_increment(self, solution):
        prob = solution.problem
        i, j, k = self.i, self.j, self.k
        t = solution.tour
        d = prob.dist
        incr = d[t[i-1]][t[j]] - d[t[i-1]][t[i]]
        incr += d[t[j-1]][t[k]] - d[t[j-1]][t[j]]
        incr += d[t[k-1]][t[i]] - d[t[k-1]][t[k]]
        return incr


class DoubleBridgeMove:
    def __init__(self, neighbourhood, i, j, k, l):
        self.neighbourhood = neighbourhood
        self.i = i
        self.j = j
        self.k = k
        self.l = l

    def __str__(self):
        return f"Double-bridge move: {self.i}, {self.j}, {self.k}, {self.l}"

    def apply_move(self, solution):
        prob = solution.problem
        # Update lower bound (really the objective value)
        solution.lb += self.objective_value_increment(solution)
        # Update tour
        i, j, k, l = self.i, self.j, self.k, self.l
        # Must replace the last slice first
        temp = solution.tour[k:l]
        solution.tour[k:l] = solution.tour[i:j]
        solution.tour[i:j] = temp
        return solution

    def objective_value_increment(self, solution):
        prob = solution.problem
        i, j, k, l = self.i, self.j, self.k, self.l
        t = solution.tour
        d = prob.dist
        incr = d[t[i-1]][t[k]] - d[t[i-1]][t[i]]
        incr += d[t[l-1]][t[j]] - d[t[j-1]][t[j]]
        incr += d[t[k-1]][t[i]] - d[t[k-1]][t[k]]
        incr += d[t[j-1]][t[l]] - d[t[l-1]][t[l]]
        return incr

# ------------------------------ Neighbourhoods ------------------------------

class Neighbourhood:
    def __init__(self, problem):
        self.problem = problem

class InsertNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        prob = self.problem
        for i in range(1, len(solution.tour)):
            for v in solution.not_visited:
                for k in (v, -v):
                    if prob.dist[0][k] != -1:
                        yield InsertMove(self, i, k)


class RemoveNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        for i in range(1, len(solution.tour)-1):
            assert self.problem.dist[solution.tour[i-1]][solution.tour[i+1]] != -1
            yield RemoveMove(self, i, solution.tour[i])

    def random_move(self, solution):
        assert self.problem == solution.problem
        if len(solution.tour) > 2:
            i = random.randrange(1, len(solution.tour)-1)
            assert self.problem.dist[solution.tour[i-1]][solution.tour[i+1]] != -1, (i, solution.tour[i-1], solution.tour[i+1])
            return RemoveMove(self, i, solution.tour[i])


class ReinsertionNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        prob = self.problem
        if len(solution.tour) == prob.n+2:
            for i in range(1, prob.n+1):
                k = solution.tour[i]
                for j in range(1, prob.n+1):
                    if i-j != 1 and i != j and prob.dist[0][k] != -1:
                        yield ReinsertionMove(self, i, j, 1)
                    if prob.dist[0][-k] != -1:
                        yield ReinsertionMove(self, i, j, -1)

    def random_move(self, solution):
        assert self.problem == solution.problem
        prob = self.problem
        if len(solution.tour) == prob.n+2:
            while True:
                s = random.randrange(-1, 2, 2)
                i = random.randrange(1, prob.n+1)
                j = random.randrange(1, prob.n+1)
                k = s * solution.tour[i]
                if  (s == -1 or i-j != 1 and i != j) and prob.dist[0][k] != -1:
                        return ReinsertionMove(self, i, j, s)

    def random_moves_without_replacement(self, solution):
        assert self.problem == solution.problem
        prob = self.problem
        if len(solution.tour) == prob.n+2:
            for x in lcg_iter(2*prob.n*prob.n):
                s = 2 * (x % 2) - 1
                x //= 2
                i = x // prob.n + 1
                j = x % prob.n + 1
                k = s * solution.tour[i]
                if  (s == -1 or i-j != 1 and i != j) and prob.dist[0][k] != -1:
                        yield ReinsertionMove(self, i, j, s)


class ThreeOptNeighbourhood(Neighbourhood):
    def moves(self, solution):
        assert self.problem == solution.problem
        prob = self.problem
        if len(solution.tour) == prob.n+2:
            for k in range(5, prob.n+2):
                for j in range(3, k-1):
                    for i in range(1, j-1):
                        yield ThreeOptMove(self, i, j, k)

    def random_move(self, solution):
        assert self.problem == solution.problem
        prob = self.problem
        if len(solution.tour) == prob.n+2:
            while True:
                # Probably inefficient but certainly unbiased
                i, j, k = sorted(random.sample(range(1, prob.n+2), 3))
                # Do not duplicate Reinsertion moves
                if j-i > 1 and k-j > 1:
                    return ThreeOptMove(self, i, j, k)

    def random_moves_without_replacement(self, solution):
        assert self.problem == solution.problem
        prob = self.problem
        if len(solution.tour) == prob.n+2:
            for x in lcg_iter((prob.n+1)*prob.n*(prob.n-1)//6):
                # Estimating k
                # Sketch of proof: Consider integers k and x such that:
                #   k*(k-1)*(k-2) <= 6*x
                # Taking the cubic root on both sides and bounding the
                # left term from below:
                #   k-2 <= pow(k*(k-1)*(k-2), 1/3) <= pow(6*x, 1/3)
                # Taking the floor on both sides
                #   k-2 <= int(pow(6*x, 1/3))
                # which implies that k <= 2 + int(pow(6*x, 1/3))
                k = 2 + int(math.pow(6*x, 1/3))
                # Find the true k
                while k*(k-1)*(k-2)//6 > x:
                    k -= 1
                y = x - k*(k-1)*(k-2)//6
                j = (1 + math.isqrt(1+8*y))//2
                i = y - j*(j-1)//2
                # Do not duplicate Reinsertion moves
                if j-i > 1 and k-j > 1:
                    yield ThreeOptMove(self, i+1, j+1, k+1)


class LocalNeighbourhood(Neighbourhood):
    def __init__(self, problem):
        self.problem = problem
        self._reinsertion_nbhood = ReinsertionNeighbourhood(problem)
        self._threeopt_nbhood = ThreeOptNeighbourhood(problem)

    def moves(self, solution):
        yield from self._reinsertion_nbhood.moves(solution)
        yield from self._threeopt_nbhood.moves(solution)

    def random_moves_without_replacement(self, solution):
        #FIXME: Formally, shuffling both types of moves together would
        #       be more correct, but this is much simpler for now
        yield from self._reinsertion_nbhood.random_moves_without_replacement(solution)
        yield from self._threeopt_nbhood.random_moves_without_replacement(solution)


class DoubleBridgeNeighbourhood(Neighbourhood):
    def random_move(self, solution):
        assert self.problem == solution.problem
        prob = self.problem
        if len(solution.tour) == prob.n+2:
            # FIXME: should moves involving single containers be included?
            # i, j, k, l = sorted(random.sample(range(1, prob.n+2), 4))
            # return DoubleBridgeMove(self, i, j, k, l)
            # Exclude moves involving single containers for now
            while True:
                i, j, k, l = sorted(random.sample(range(1, prob.n+2), 4))
                if j-i > 1 and k-j > 1 and l-k > 1:
                    return DoubleBridgeMove(self, i, j, k, l)


# ---------------------------------- Solution --------------------------------

class Solution:
    def __init__(self, problem, tour, not_visited, lb):
        self.problem = problem
        self.tour = tour
        self.not_visited = not_visited
        self.lb = lb

    def __str__(self):
        prob = self.problem
        tab = []
        length = 0
        nxt = self.tour[0]
        for i in range(1, len(self.tour)):
            prv, nxt = nxt, self.tour[i]
            length += prob.dist[prv][nxt]
            tab.append((i, prv, nxt, prob.dist[prv][nxt], length))
        return tabulate(tab, headers=["step", "from", "to", "dist", "length"])

    def copy_solution(self):
        return Solution(self.problem,
            self.tour.copy(),
            self.not_visited.copy(),
            self.lb)

    def objective_value(self):
        if len(self.not_visited) == 0:
            return self.lb

    def lower_bound(self):
        return self.lb

    def to_textio(self, f):
        if len(self.not_visited) == 0:
            f.write('\n'.join(f"{abs(v)} {int(v < 0)}" for v in self.tour[1:-1]))
            # Alternatively, prettier formating
            # out = ((abs(v), int(v<0)) for v in self.tour[1:-1])
            # f.write(tabulate(out, tablefmt='plain'))
            f.write('\n')

# ---------------------------------- Problem --------------------------------

# Full model with 3-opt local-search neighbourhood and double-bridge
# perturbation
class Problem:
    def __init__(self, dist):
        self.n = len(dist) // 2
        self.dist = tuple(tuple(row) for row in dist)
        self.c_nbhood = None
        self.d_nbhood = None
        self.l_nbhood = None
        self.p_nbhood = None

    def __str__(self):
        return(f"Problem instance: dist =\n{tabulate(self.dist, tablefmt='plain')}")

    def construction_neighbourhood(self):
        if self.c_nbhood is None:
            self.c_nbhood = InsertNeighbourhood(self)
        return self.c_nbhood

    def destruction_neighbourhood(self):
        if self.d_nbhood is None:
            self.d_nbhood = RemoveNeighbourhood(self)
        return self.d_nbhood

    def local_neighbourhood(self):
        if self.l_nbhood is None:
            self.l_nbhood = LocalNeighbourhood(self)
        return self.l_nbhood

    #FIXME: This is not specified by the ROAR-NET API (yet?)
    def perturbation_neighbourhood(self):
        if self.p_nbhood is None:
            self.p_nbhood = DoubleBridgeNeighbourhood(self)
        return self.p_nbhood

    @classmethod
    def from_textio(cls, f):
        """
        Create a problem from a text I/O source `f`
        """
        n = int(f.readline())
        dist = [(2*n+1) * [-1] for _ in range(2*n+1)]
        # NOTE: The distance between the depot to the waste-treatment
        # plant is not provided by the instance, so it is taken as 0 in
        # this model. This is not an issue as long as this value is a
        # constant. Furthermore, both the depot and the treatment plant
        # are represented by position 0. Note that vehicles can never
        # return directly from a waste container to the depot, nor from
        # the treatment plant to a waste container.
        dist[0][0] = 0
        dist[0][1:n+1] = map(int, f.readline().split())
        dist[0][-1:-n-1:-1] = map(int, f.readline().split())
        for i, d in zip(range(1, n+1), map(int, f.readline().split())):
            dist[i][0] = d
        for i, d in zip(range(1, n+1), map(int, f.readline().split())):
            dist[-i][0] = d
        for i in range(1, n+1):
            dist[i][1:n+1] = map(int, f.readline().split())
        for i in range(1, n+1):
            dist[i][-1:-n-1:-1] = map(int, f.readline().split())
        for i in range(1, n+1):
            dist[-i][-1:-n-1:-1] = map(int, f.readline().split())
        for i in range(1, n+1):
            dist[-i][1:n+1] = map(int, f.readline().split())
        return cls(dist)

    def empty_solution(self):
        # NOTE: The empty route connects the depot directly to the
        # treatment plant. Both are represented by 0.
        return Solution(self, [0, 0], set(range(1, self.n+1)), self.dist[0][0])

    def random_solution(self):
        tour = random.sample(range(1, self.n+1), self.n)
        tour.insert(0, 0)
        tour.append(0)
        obj_val = 0
        for i in range(1, self.n+1):
            if self.dist[0][tour[i]] == -1:
                assert self.dist[0][-tour[i]] != -1
                tour[i] = -tour[i]
            elif self.dist[0][-tour[i]] != -1 and random.random() < 0.5:
                tour[i] = -tour[i]
            obj_val += self.dist[tour[i-1]][tour[i]]
        obj_val += self.dist[tour[self.n]][tour[self.n+1]]
        return Solution(self, tour, set(), obj_val)

# Basic model, with reinsertion neighbourhood for local-search and perturbation
class Problem0(Problem):
    def local_neighbourhood(self):
        if self.l_nbhood is None:
            self.l_nbhood = ReinsertionNeighbourhood(self)
        return self.l_nbhood

    def perturbation_neighbourhood(self):
        if self.p_nbhood is None:
            self.p_nbhood = ReinsertionNeighbourhood(self)
        return self.p_nbhood

# Basic model with double-bridge perturbation
class Problem1(Problem):
    def local_neighbourhood(self):
        if self.l_nbhood is None:
            self.l_nbhood = ReinsertionNeighbourhood(self)
        return self.l_nbhood

# Full model with limited 3-opt perturbation (instead of double bridge)
class Problem2(Problem):
    def perturbation_neighbourhood(self):
        if self.p_nbhood is None:
            self.p_nbhood = ThreeOptNeighbourhood(self)
        return self.p_nbhood

