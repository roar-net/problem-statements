#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: © 2025 Authors of the roar-net-api-py project <https://github.com/roar-net/roar-net-api-py/blob/main/AUTHORS>
#
# SPDX-License-Identifier: Apache-2.0


import argparse
import json
import logging
import sys
import textwrap
from dataclasses import dataclass
from pathlib import Path
from typing import Self, TextIO, Optional

import jsonschema

log = logging.getLogger(__name__)


# ---------------------------------- Problem --------------------------------
@dataclass(
    init=False,
    repr=True,
    eq=True,
    order=False,
    unsafe_hash=False,
    frozen=True,
    match_args=False,
    kw_only=False,
    slots=False,
    weakref_slot=False,
)
class AttrDict:
    def __init__(self, d: dict):
        for k, v in d.items():
            object.__setattr__(self, k, v)

    def __str__(self) -> str:
        return "\n".join(
            f"{k}: {v}" for k, v in self.__dict__.items() if not k.startswith("_")
        )


class Problem:
    def __init__(self, d: dict):
        self.data = AttrDict(d)

        self.name = self.data.name
        self.max_time = self.data.max_time
        self.nodes = {n["label"]: n for n in self.data.nodes}
        self.vehicles = {v["id"]: v for v in self.data.vehicles}
        self.depots = {d["label"]: d for d in self.data.depots}
        self.dwelling_nodes = {v["home"]: v for v in self.data.vehicles}
        self.arcs = {tuple(a["arc"]): a for a in self.data.A}
        self.arcs_required = {tuple(a["arc"]): a for a in self.data.A_R}
        self.edges_required = {tuple(a["edge"]): a for a in self.data.E_R}
        self.all_links = (
            set(self.arcs.keys())
            | set(self.arcs_required.keys())
            | set(self.edges_required.keys())
        )
        self.all_links |= {(a[1], a[0]) for a in self.edges_required.keys()}
        self.U = {n["label"]: n for n in self.data.U}

    @classmethod
    def from_textio(cls, f: TextIO) -> Self:
        """
        Create a problem from a text I/O source `f`
        """
        data = json.load(f)
        # Load JSON schema
        with open("support/schema_instance.json", "r") as f:
            schema = json.load(f)
        try:
            jsonschema.validate(instance=data, schema=schema)
            log.info("JSON is valid")
        except jsonschema.ValidationError as ve:
            log.info(f"Validation error: {ve.message}")
            sys.exit(0)
        except jsonschema.SchemaError as se:
            log.info(f"Schema error: {se.message}")
            sys.exit(0)
        return cls(data)  # , data.name)

    def statistics(self) -> None:
        data = self.data
        print(
            "Nodes %d, arcs %d, of which %d required and %d alternative pairs required"
            % (len(data.nodes), len(data.A), len(data.A_R), len(data.E_R))
        )

        tot_length = sum(d["len"] for d in data.A)
        print("Total sum of lengths of all arcs available", tot_length)

        tot_length = sum(d["len"] for d in data.A_R) + sum(d["len"] for d in data.E_R)
        print("Total sum of lengths of the arcs and edges to salt", tot_length)

        tot_demand = sum(d["dem"] for d in data.A_R) + sum(d["dem"] for d in data.E_R)
        print("Total required demand", tot_demand)

        capacity = sum(v["capacity"] for v in data.vehicles)
        print("Total capacity", capacity)

        size_U = len(data.U)
        print("U-turn-allowed nodes", size_U)


class Solution:
    def __init__(self, problem: Problem, routes: dict = None) -> None:
        self.problem = problem
        self.routes = routes

    @classmethod
    def from_textio(cls, problem: Problem, f: TextIO) -> Self:
        schema = {
            "$schema": "http://json-schema.org/schema#",
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "vehicle": {"type": "string"},
                    "route": {
                        "type": "array",
                        "items": {
                            "type": "object",
                            "properties": {
                                "arc": {
                                    "type": "array",
                                    "items": {"type": ["null", "string"]},
                                },
                                "salted": {"type": "boolean"},
                            },
                            "required": ["arc", "salted"],
                        },
                    },
                },
                "required": ["route", "vehicle"],
            },
        }

        data = json.load(f)

        try:
            jsonschema.Draft202012Validator.check_schema(schema)
            jsonschema.validate(data, schema, cls=jsonschema.Draft202012Validator)
        except jsonschema.exceptions.ValidationError as e:
            log.error(f"Validation error: {e.message}")
            log.error(f"Data: {data}")
            raise e
        except jsonschema.exceptions.SchemaError as e:
            log.error(f"Schema error: {e.message}")
            raise e
        log.info("Reading input solution succeeded.")

        return cls(problem, data)

    def is_feasible(self) -> bool:
        arcs_required = set(self.problem.arcs_required.keys())
        edges_required = set(self.problem.edges_required.keys())
        for r in self.routes:
            vehicle = r["vehicle"]
            route = r["route"]
            log.info(f"Checking route for vehicle {vehicle}")
            # Check if the vehicle exists in the problem
            if vehicle not in self.problem.vehicles:
                log.info(f"Vehicle {vehicle} not found in problem vehicles.")
                return False
            # Check if the route starts at vehicles' dwelling place
            # if route[0]["arc"][0] != self.problem.vehicles[vehicle]["home"]:
            #    log.info(
            #        f"Route for vehicle {vehicle} does not start at its dwelling place."
            #    )
            #    return False
            # if route[-1]["arc"][1] not in self.problem.depots:
            #    log.info(
            #        f"Route for vehicle {vehicle} does not end at a refilling depot."
            #    )
            #    return False
            # Check if the route contains only valid links
            for i in range(len(r)):
                if tuple(route[i]["arc"]) not in self.problem.all_links:
                    log.info(
                        f"Route for vehicle {vehicle} contains an invalid arc: {route[i]['arc']}."
                    )
                    return False
            # Check if the route covers required arcs and edges and does not exceed vehicle capacity
            residual_capacity: float = self.problem.vehicles[vehicle]["capacity"]
            for i in range(len(route)):
                _arc = tuple(route[i]["arc"])
                _arc_inv = (_arc[1], _arc[0])
                if _arc in arcs_required and route[i]["salted"]:
                    arcs_required.remove(_arc)
                    residual_capacity -= self.problem.arcs_required[_arc]["dem"]
                elif _arc in edges_required and route[i]["salted"]:
                    edges_required.remove(_arc)
                    residual_capacity -= self.problem.edges_required[_arc]["dem"]
                elif _arc_inv in edges_required and route[i]["salted"]:
                    edges_required.remove(_arc_inv)
                    residual_capacity -= self.problem.edges_required[_arc_inv]["dem"]

                if residual_capacity < 0:
                    log.info(f"Route for vehicle {vehicle} exceeds its capacity.")
                    return False
                if route[i]["arc"][1] in self.problem.depots:
                    # Reset capacity at refilling depot
                    residual_capacity = min(
                        self.problem.vehicles[vehicle]["capacity"],
                        residual_capacity
                        + self.problem.depots[route[i]["arc"][1]]["refill"],
                    )
                # Check if a U-turn has occurred at a node where it is not allowed
                if (
                    i < len(route) - 1
                    and route[i]["arc"][1] in self.problem.nodes
                    and route[i]["arc"][1] not in self.problem.U
                ):
                    if route[i]["arc"] == route[i + 1]["arc"]:
                        log.info(
                            f"U-turn at node {route[i]} is not allowed for vehicle {vehicle}."
                        )
                        return False
            source = self.problem.vehicles[vehicle]["home"]
            arcs = [tuple(arc["arc"]) for arc in route]
            # checking connectivity
            connected, path = self.__pairing_algorithm(source, arcs)
            if not connected:
                return False
            # else:
            #    log.info(f"{path}")

        # Check max duration
        if self.problem.max_time is not None:
            duration = 0
            for i in range(len(route)):
                arc = tuple(route[i]["arc"])
                if arc in self.problem.arcs:
                    duration -= self.problem.arcs[arc]["time"]
                elif arc in self.problem.arcs_required:
                    duration -= self.problem.arcs_required[arc]["time"]
                elif arc in self.problem.edges_required:
                    duration -= self.problem.edges_required[arc]["time"]
                elif (arc[1], arc[0]) in self.problem.edges_required:
                    duration -= self.problem.edges_required[(arc[1], arc[0])]["time"]

            if duration > self.problem.max_time:
                log.info(
                    f"The route exceeds by {duration - self.problem.max_time} the maximum duration"
                )
                return False

        # Check if all required arcs and edges are covered
        if len(arcs_required) > 0:
            log.info(
                f"Route for vehicle {vehicle} does not cover all required arcs: {arcs_required}."
            )
            return False
        if len(edges_required) > 0:
            log.info(
                f"Route for vehicle {vehicle} does not cover all required edges: {edges_required}."
            )
            return False
        # Check if continuous path

        return True

    def __pairing_algorithm(self, source: str, arcs: list[tuple]) -> list:
        path = [source]
        while len(arcs) > 0:
            found = False
            for arc in arcs:
                if arc[0] == source:
                    found = True
                    source = arc[1]
                    path += [source]
                    arcs.remove(arc)
                    break
            if not found:
                last_node = source
                if last_node not in self.problem.depots:
                    log.info(
                        "Route does not end at a refilling depot or start at a dwelling place."
                    )
                    return False
                while len(arcs) > 0:
                    path_2 = self.__remove_cycle(arcs, path)
                    if (
                        path_2 is not None and path_2[0] == path_2[-1]
                    ):  # it is really a cycle
                        i = path.index[path_2[0]]
                        path = path[:i] + path_2 + path[i + 1 :]
                    else:
                        log.info("Route is disconnected.")
                        return False, path
        if len(arcs) == 0:
            last_node = source
            if last_node not in self.problem.depots:
                log.info("Route does not end at a refilling depot.")
                return False, path
        return True, path

    def __remove_cycle(self, arcs: list[tuple], path: list) -> list | None:
        # if len(arcs)==1
        # print(path, arcs)
        log.info("Checking for cycles")
        source = None
        for arc in arcs:
            if arc[0] in path:
                source = arc[0]
                break
        if source is None:
            log.info("while checking for cycles detected disconnected route")
            return None
        cycle = [source]
        while len(arcs) > 0:
            found = False
            for arc in arcs:
                if arc[0] == source:
                    found = True
                    source = arc[1]
                    cycle += [source]
                    arcs.remove(arc)
                    break
            if not found:
                return cycle
        return cycle

    def objective_value(self) -> Optional[float]:
        length = 0
        for r in self.routes:
            route = r["route"]
            for i in range(len(route)):
                arc = tuple(route[i]["arc"])
                if arc in self.problem.arcs:
                    length += self.problem.arcs[arc]["len"]
                elif arc in self.problem.arcs_required:
                    length += self.problem.arcs_required[arc]["len"]
                elif arc in self.problem.edges_required:
                    length += self.problem.edges_required[arc]["len"]
                elif (arc[1], arc[0]) in self.problem.edges_required:
                    length += self.problem.edges_required[(arc[1], arc[0])]["len"]

        return length


def parse_cmd_line():
    s = textwrap.dedent("""\
                    Example:
                    python3 src/main.py data/gualandi/gualandi.json -s data/gualandi/gualandi_ransol.json 
                    See -h for explanation
                    """)

    parser = argparse.ArgumentParser(description="Salt spreading", epilog=s)
    # Positional arguments
    parser.add_argument(
        "instance_file", help="The input data in compliant json format", type=str
    )

    parser.add_argument(
        "-s",
        "--solution",
        metavar="InSolution",
        dest="input_solution_file",
        type=Path,
        action="store",
        required=True,
        nargs="?",
        default=None,
        help="a file containing the solution in json format",
    )

    args = parser.parse_args()

    return args


def main(args: None | argparse.Namespace = None) -> None:
    if args is None:
        args = parse_cmd_line()

    logging.basicConfig(
        stream=sys.stderr, level="INFO", format="%(levelname)s;%(asctime)s;%(message)s"
    )

    with open(args.instance_file, "r") as file:
        problem = Problem.from_textio(file)

    problem.statistics()

    # read the solution from a file
    with open(args.input_solution_file, "r") as file:
        solution = Solution.from_textio(problem, file)

    if solution.is_feasible:
        log.info("Initial solution is feasible.")
        length = solution.objective_value()
        log.info(f"The total length is: {length}")


if __name__ == "__main__":
    args = parse_cmd_line()
    main(args)
