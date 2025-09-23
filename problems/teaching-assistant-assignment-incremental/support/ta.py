#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: © 2025 Authors of the roar-net-api-py project <https://github.com/roar-net/roar-net-api-py/blob/main/AUTHORS>
#
# SPDX-License-Identifier: Apache-2.0

from __future__ import annotations

import json
import logging
import random
import sys
from collections.abc import Iterable
from logging import getLogger
from typing import Optional, Protocol, Self, TextIO, TypeVar, final

from roar_net_api.operations import (
    SupportsApplyMove,
    SupportsConstructionNeighbourhood,
    SupportsCopySolution,
    SupportsEmptySolution,
    SupportsLocalNeighbourhood,
    SupportsLowerBound,
    SupportsLowerBoundIncrement,
    SupportsMoves,
    SupportsObjectiveValue,
    SupportsObjectiveValueIncrement,
    SupportsRandomMove,
    SupportsRandomMovesWithoutReplacement,
)

import ta_utils
from ta_classes import SessionOccurrence
from ta_classes import TeachingAssistant

log = getLogger(__name__)


class _SupportsLT(Protocol):
    def __lt__(self, other: Self) -> bool: ...


_T = TypeVar("_T", bound=_SupportsLT)


# ---------------------------------- Solution --------------------------------


@final
class Solution(SupportsCopySolution, SupportsObjectiveValue, SupportsLowerBound):
    def __init__(self, problem: Problem, mapping: dict[SessionOccurrence, list[TeachingAssistant]],
                 unused_tas: list[TeachingAssistant], unused_session_occurrences: list[SessionOccurrence], lb: int):
        assert problem is not None
        assert mapping is not None
        assert unused_tas is not None
        assert unused_session_occurrences is not None
        assert lb is not None
        self.problem = problem
        self.mapping = mapping
        self.unused_tas = unused_tas
        self.unused_session_occurrences = unused_session_occurrences
        self.lb = lb

    def __str__(self) -> str:
        return " ".join(map(str, self.mapping))

    @property
    def is_feasible(self) -> bool:
        # If there are any unused/non-mapped session occurrences -> infeasible
        if len(self.unused_session_occurrences) != 0:
            return False

        # Session occurrence checks:
        # Check for every session occurrence that there are exactly as many TAs as needed
        for so in self.problem.session_occurrences:
            # If there is no mapping at all -> infeasible
            if so not in self.mapping:
                return False

            # Check number of assigned TAs
            if len(self.mapping[so]) != so.number_of_tas:
                return False

            # Every assigned TA must have at least a qualification != 0
            for ta in self.mapping[so]:
                if not so in ta.qualifications:
                    return False
                if ta.qualifications[so] == 0:
                    return False

        # TA checks:
        for ta in self.problem.tas:
            # Calculate time
            total_time = 0
            weekly_time = {}
            found_session_occurrences = []

            # Find working time (weekly and yearly/total) as well as assigned session occurrences
            for so in self.mapping.keys():
                if ta in self.mapping[so]:
                    found_session_occurrences.append(so)
                    total_time += so.hours_paid_per_occurrence
                    if so.week not in weekly_time:
                        weekly_time[so.week] = 0
                    weekly_time[so.week] += so.hours_paid_per_occurrence

            # Check weekly time
            for w in weekly_time.keys():
                if weekly_time[w] > ta.max_hours_per_week:
                    return False

            # Check yearly/total time
            if total_time > ta.max_hours_per_year:
                return False

            # Check conflicting assignments
            if ta_utils.check_occurrences_for_conflicts(found_session_occurrences):
                return False

            # Check blocked dates
            for so in self.mapping.keys():
                if ta in self.mapping[so]:
                    if ta_utils.is_ta_bocked_in_so(ta, so):
                        return False

        # If no violation was found, everything is fine and the solution is valid/feasible
        return True

    def to_textio(self, f: TextIO) -> None:
        assert f is not None
        f.write("NAME : %s\nTYPE : TA\n" % self.problem.name)
        f.write("#SessionOccurrences : %d\n" % len(self.problem.session_occurrences))
        f.write("#TeachingAssistants : %d\n" % len(self.problem.tas))
        for so in self.mapping.keys():
            f.write(so.name + " -> " + " ".join(str(ta.name) + " " for ta in self.mapping[so]) + "\n")
        f.write("EOF\n")

    def to_json(self, f: TextIO) -> None:
        assert f is not None
        data = {"name": self.problem.name}

        # session occurrences
        session_occurrences = []
        for so in self.problem.session_occurrences:
            so_dict = {}
            so_dict["name"] = so.name
            so_dict["date_start"] = so.date_start
            so_dict["date_end"] = so.date_end
            so_dict["number_of_tas"] = so.number_of_tas
            so_dict["hours_paid_per_occurrence"] = so.hours_paid_per_occurrence
            so_dict["week"] = so.week
            session_occurrences.append(so_dict)
        data["sessionOccurrences"] = session_occurrences

        # TAs
        tas = []
        for ta in self.problem.tas:
            ta_dict = {}
            ta_dict["name"] = ta.name
            qualifications = {}
            for q in ta.qualifications:
                qualifications[q.name] = -1 * ta.qualifications[q]
            ta_dict["qualifications"] = qualifications
            ta_dict["max_hours_per_week"] = ta.max_hours_per_week
            ta_dict["max_hours_per_year"] = ta.max_hours_per_year
            ta_dict["blocked_dates"] = ta.blocked_dates
            tas.append(ta_dict)
        data["tas"] = tas

        # Mappings
        mappings = {}
        for so in self.mapping.keys():
            mappings[so.name] = []
            for ta in self.mapping[so]:
                mappings[so.name].append(ta.name)
        data["mappings"] = mappings

        j = json.dumps(data, indent=4)
        f.write(j)

    @classmethod
    def from_json(cls, path: str) -> Self:
        assert path is not None

        # problem
        problem = Problem.from_json(path)
        with open(path) as f:
            imported = json.load(f)

            # mapping
            mappings = {}
            for so in imported["mappings"]:
                mappings[so] = imported["mappings"][so]

            # unused TAs
            unused_tas = problem.tas.copy()
            for so in mappings:
                for ta in mappings[so]:
                    if ta in unused_tas:
                        unused_tas.remove(ta)

            # unused session occurrences
            unused_session_occurrences = []
            for so in problem.session_occurrences:
                if so not in mappings:
                    unused_session_occurrences.append(so)

            return cls(problem, mappings, unused_tas, unused_session_occurrences, 0)

    def copy_solution(self) -> Self:
        return self.__class__(self.problem, self.mapping.copy(), self.unused_tas.copy(),
                              self.unused_session_occurrences.copy(), self.lb)

    def objective_value(self) -> Optional[int]:
        if self.is_feasible:
            return self.lb
        return None

    def lower_bound(self) -> int:
        return self.lb


# ----------------------------------- Moves -----------------------------------


@final
class AddMove(SupportsApplyMove[Solution], SupportsLowerBoundIncrement[Solution]):
    def __init__(self, neighbourhood: AddNeighbourhood, so: SessionOccurrence, ta: TeachingAssistant):
        assert neighbourhood is not None
        assert so is not None
        assert ta is not None
        # It is only allowed to add TAs with a qualification for the respective session occurrence
        assert ta_utils.is_ta_qualified_for_so(ta, so)
        # It is only allowed to add TAs when they do not have the date blocked
        assert not ta_utils.is_ta_bocked_in_so(ta, so)
        self.neighbourhood = neighbourhood
        self.so = so
        self.ta = ta

    def apply_move(self, solution: Solution) -> Solution:
        # Update lower bound: += qualification of the newly added TA mapping
        solution.lb += self.ta.qualifications.get(self.so)
        # Calculate and add possible penalty cost (for a new assignment not previously chosen)
        solution.lb += ta_utils.get_same_assignment_cost(solution.problem, self.ta, self.so)
        # Update solution
        if self.so not in solution.mapping:
            solution.mapping[self.so] = []
        solution.mapping[self.so].append(self.ta)
        solution.unused_session_occurrences.remove(self.so)
        if self.ta in solution.unused_tas:
            solution.unused_tas.remove(self.ta)
        return solution

    def lower_bound_increment(self, solution: Solution) -> float:
        # Lb increment: qualification cost + possible penalty cost (for a new assignment not previously chosen)
        return self.ta.qualifications.get(self.so) + ta_utils.get_same_assignment_cost(solution.problem, self.ta, self.so)


@final
class NewTaMove(SupportsApplyMove[Solution], SupportsObjectiveValueIncrement[Solution]):
    def __init__(self, neighbourhood: NewTaNeighbourhood, so: SessionOccurrence, new_ta: TeachingAssistant):
        assert neighbourhood is not None
        assert so is not None
        assert new_ta is not None
        # The new TA must have at least some qualification for the session occurrence
        assert ta_utils.is_ta_qualified_for_so(new_ta, so)
        # It is only allowed to add TAs when they do not have the date blocked
        assert not ta_utils.is_ta_bocked_in_so(new_ta, so)
        self.neighbourhood = neighbourhood
        self.so = so
        self.new_ta = new_ta

        # The old TA must be chosen randomly once
        self.old_ta = random.choice(solution.mapping[self.so])

    def apply_move(self, solution: Solution) -> Solution:
        # There must be at least one previously assigned TA
        assert len(solution.mapping[self.so]) > 0

        # Update/decrement the lb by removing the previous mappings
        solution.lb -= self.old_ta.qualifications.get(self.so)
        # Calculate and subtract possible penalty cost (for a new assignment not previously chosen)
        solution.lb -= ta_utils.get_same_assignment_cost(solution.problem, self.old_ta, self.so)

        # Replace the old TA with the new one
        solution.mapping[self.so].remove(self.old_ta)
        solution.mapping[self.so].append(self.new_ta)

        # Update lb with the new mappings
        solution.lb += self.new_ta.qualifications.get(self.so)
        # Calculate and add possible penalty cost (for a new assignment not previously chosen)
        solution.lb += ta_utils.get_same_assignment_cost(solution.problem, self.new_ta, self.so)
        return solution

    def objective_value_increment(self, solution: Solution) -> float:
        incr = 0
        incr -= self.old_ta.qualifications.get(self.so)
        incr += self.new_ta.qualifications.get(self.so)
        # Calculate and subtract possible penalty cost (for a new assignment not previously chosen)
        incr -= ta_utils.get_same_assignment_cost(solution.problem, self.old_ta, self.so)
        # Calculate and add possible penalty cost (for a new assignment not previously chosen)
        incr += ta_utils.get_same_assignment_cost(solution.problem, self.new_ta, self.so)
        return incr


# ------------------------------- Neighbourhood ------------------------------


@final
class AddNeighbourhood(SupportsMoves[Solution, AddMove]):
    def __init__(self, problem: Problem):
        self.problem = problem

    def moves(self, solution: Solution) -> Iterable[AddMove]:
        assert self.problem == solution.problem
        for so in solution.unused_session_occurrences:
            for ta in solution.unused_tas:
                if ta_utils.is_ta_qualified_for_so(ta, so):
                    if not ta_utils.is_ta_bocked_in_so(ta, so):
                        yield AddMove(self, so, ta)


# Note: the ROAR-NET API glossary states that all *local* neighbourhoods must be feasible.
# Therefore, this neighbourhood only constructs moves that leave the solution in a feasible state.
@final
class NewTaNeighbourhood(
    SupportsMoves[Solution, NewTaMove],
    SupportsRandomMovesWithoutReplacement[Solution, NewTaMove],
    SupportsRandomMove[Solution, NewTaMove],
):
    def __init__(self, problem: Problem):
        self.problem = problem

    def moves(self, solution: Solution) -> Iterable[NewTaMove]:
        assert self.problem == solution.problem
        # This is only meant to be used as a local neighbourhood, so solution should be feasible
        assert solution.is_feasible

        # All assignable TAs should be added to the neighbourhood
        for so in self.problem.session_occurrences:
            for ta in self.problem.tas:
                if ta_utils.is_ta_assignable_to_so(solution, ta, so):
                    if not ta_utils.is_ta_bocked_in_so(ta, so):
                        yield NewTaMove(self, so, ta)

    def random_moves_without_replacement(self, solution: Solution) -> Iterable[NewTaMove]:
        assert self.problem == solution.problem
        all_sos = solution.problem.session_occurrences.copy()
        random.shuffle(all_sos)
        for so in all_sos:
            all_tas = solution.problem.tas.copy()
            random.shuffle(all_tas)
            for ta in all_tas:
                # The TA must be assignable
                if ta_utils.is_ta_assignable_to_so(solution, ta, so):
                    # The TA must not be blocked at the session occurrence's date
                    if not ta_utils.is_ta_bocked_in_so(ta, so):
                        yield NewTaMove(self, so, ta)

    def random_move(self, solution: Solution) -> Optional[NewTaMove]:
        return next(iter(self.random_moves_without_replacement(solution)), None)


# ---------------------------------- Problem --------------------------------


@final
class Problem(
    SupportsConstructionNeighbourhood[AddNeighbourhood],
    SupportsLocalNeighbourhood[NewTaNeighbourhood],
    SupportsEmptySolution[Solution],
):
    def __init__(self, session_occurrences: list[SessionOccurrence], tas: list[TeachingAssistant], name: str,
                 orig_mappings: dict[SessionOccurrence, list[TeachingAssistant]]):
        assert session_occurrences is not None
        assert tas is not None
        assert name is not None
        assert orig_mappings is not None
        self.session_occurrences = session_occurrences
        self.tas = tas
        self.name = name
        self.orig_mappings = orig_mappings
        self.n = len(self.session_occurrences)
        self.c_nbhood: Optional[AddNeighbourhood] = None
        self.l_nbhood: Optional[NewTaNeighbourhood] = None

    def __str__(self) -> str:
        out: list[str] = ["Session occurrences:\n"]
        for so in self.session_occurrences:
            out.append(" ".join(so.name))
        out.append("Teaching assistants:\n")
        for ta in self.tas:
            out.append(" ".join(ta.name))
        return "\n".join(out)

    def construction_neighbourhood(self) -> AddNeighbourhood:
        if self.c_nbhood is None:
            self.c_nbhood = AddNeighbourhood(self)
        return self.c_nbhood

    def local_neighbourhood(self) -> NewTaNeighbourhood:
        if self.l_nbhood is None:
            self.l_nbhood = NewTaNeighbourhood(self)
        return self.l_nbhood

    @classmethod
    def from_json(cls, path: str) -> Self:
        assert path is not None
        with open(path) as f:
            imported = json.load(f)

            # Session occurrences
            imported_session_occurrences = {}
            for so in imported["sessionOccurrences"]:
                imported_session_occurrences[so["name"]] = SessionOccurrence(so["name"], so["date_start"],
                                                                             so["date_end"], so["number_of_tas"],
                                                                             so["hours_paid_per_occurrence"],
                                                                             so["week"])

            # TAs
            imported_tas = []
            for ta in imported["tas"]:
                leftover_session_occurrences = imported_session_occurrences.copy()
                qualifications = {}
                for q in ta["qualifications"].keys():
                    # The `qualification` value must be negative because the ROAR-NET API only minimizes the obj value.
                    # (Multiplying a maximization problem with (-1) results in a minimization problem.)
                    qualifications[imported_session_occurrences[q]] = -1 * ta["qualifications"].get(q)
                    leftover_session_occurrences.pop(q)
                # Fill all other (non-)qualifications up with '0'
                for q in leftover_session_occurrences.values():
                    qualifications[q] = 0
                blocked_dates = []
                if "blocked_dates" in ta:
                    for blocked_date in ta["blocked_dates"]:
                        blocked_dates.append(blocked_date)
                new_ta = TeachingAssistant(ta["name"], qualifications, ta["max_hours_per_week"],
                                           ta["max_hours_per_year"], blocked_dates)
                imported_tas.append(new_ta)

            # mapping
            mappings = {}
            for so in imported["mappings"]:
                mappings[so] = imported["mappings"][so]

            return cls(list(imported_session_occurrences.values()), imported_tas, imported["name"], mappings)

    def empty_solution(self) -> Solution:
        # An empty solution is just a solution with no mappings, all TAs, all session occurrences, and a lb of 0
        return Solution(self, {}, self.tas.copy(), self.session_occurrences.copy(), 0)


if __name__ == "__main__":
    import roar_net_api.algorithms as alg

    # Configure logging
    logging.basicConfig(stream=sys.stdout, level="INFO", format="%(levelname)s;%(asctime)s;%(message)s")

    # # Load the previously calculated batch solution
    # solution = Solution.from_json('./ta_solution.json')

    # Load a local JSON file with a problem instance
    problem = Problem.from_json('./ta_solution.json')

    # Run greedy construction to get an initial solution
    solution = alg.greedy_construction(problem)
    # solution = alg.beam_search(problem, bw=10)
    # solution = alg.grasp(problem, 30.0)
    log.info(f"Objective value after constructive search: {solution.objective_value()}")

    log.info("Initial solution:")
    solution.to_textio(sys.stdout)

    # Run simulated annealing to improve the previous solution
    solution = alg.sa(problem, solution, 2.0, 30.0)
    # solution = alg.rls(problem, solution, 10.0)
    # solution = alg.best_improvement(problem, solution)
    # solution = alg.first_improvement(problem, solution)
    log.info(f"Objective value after local search: {solution.objective_value()}")

    # Print the final solution to stdout
    log.info("Final solution:")
    solution.to_textio(sys.stdout)

    # Export the final solution as JSON file
    with open("./ta_solution_reopt.json", "w") as f:
        solution.to_json(f)
