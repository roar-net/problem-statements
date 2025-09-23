<!--
SPDX-FileCopyrightText: 2025 Maximilian Kratz <maximilian.kratz@es.tu-darmstadt.de>

SPDX-License-Identifier: CC-BY-4.0
-->

<!-- Replace the comment above with your licence information for your problem
statement. Consider all copyright holders and contributors. -->

<!-- According to the copyright and licensing policy of ROAR-NET original
problem statements contributed to this repository shall be licensed under the
CC-BY-4.0 licence. In some cases CC-BY-SA-4.0 might be accepted, e.g., if the
problem is based upon an existing problem licensed under those terms. Please
provide a clear justification when opening the pull request if the problem is
not licensed under CC-BY-4.0 -->

# Teaching Assistant Assignment

Maximilian Kratz, Real-Time Systems Lab, Technical University of Darmstadt, Darmstadt, Germany

<!-- Put two empty spaces at the end of each author line except the last for
proper formatting -->

Copyright 2025 Maximilian Kratz <maximilian.kratz@es.tu-darmstadt.de>.

This document is licensed under CC-BY-4.0.

<!-- Complete the above accordingly. Copyright and licensing information must be
consistent with the comment at the beginning of the markdown file -->

## Introduction

The assignment of Teaching Assistants (TAs) to courses and sessions is a problem that occurs in universities regularly.
This problem description is based on a real-world problem, where the goal is to determine a valid assignment plan for several courses and the TAs in a given semester.
Therefore, multiple constraints (e.g., the maximum weekly work time of a TA) must be considered.

## Task

The problem consists in determining the optimal TA assignment to a set of university session (occurrences), while fulfilling different constraints and maximizing the quality of the assignments (in terms of TA qualifications).

## Detailed description

This section explains what parameters characterize a problem instance, what characterizes a solution, how a solution is evaluated, and the solution feasibility constraints.

### Problem instance parameters

- `session_occurrences`: List of all session occurrences in the problem. A session occurrence is characterized by the following parameters:
    - `name`: The name of the session. Example: `Computer Science 101`
    - `date_start`: The start date of the session as string, e.g.: `2025-09-10 08:00:00`
    - `date_end`: The end date of the session as string, e.g.: `2025-09-10 09:30:00`
    - `number_of_tas`: The desired number of TAs that must be assigned to this session occurrence. Example: `2`
    - `hours_paid_per_occurrence`: The number of hours a TA gets paid for when giving the session. Example: `1`
    - `week`: The number of the week within the semester the session will occur in. Example: `1`
- `tas`: List of all TAs in the problem. A TA is characterized by the following parameters:
    - `name`: The name of the TA. Example: `Jane Doe`
    - `qualifications`: A list of tuples of qualifications of this particular TA. The key of an entry should be the `name` of a session occurrence and the corresponding value is one of `0` (not qualified to give the course), `1` (reasonably qualified to give the course), and `2` (very qualified to give the course).
    - `max_hours_per_week`: The maximum amount of hours this TA is allowed to work per week. Example: `10`
    - `max_hours_per_year`: The maximum amount of hours this TA is allowed to work per year/semester/planning horizon. Example: `300`
    - `blocked_dates`: A list of blocked dates, i.e., dates that this TA is not available at all. Example: `["2025-09-10"]`
- `name`: A given name for a problem instance. (Can be freely chosen.) Example: `Small TA example problem`

### Solution characterization

A solution to the described problem is characterized by the following details:

- `problem`: The problem to be solved. The problem consists of a set of session occurrences and TAs as described above.
- `mapping`: Map of key value pairs that represent the assignment of TAs to session occurrences. The keys represent all sesion occurrences while the value of the map consists of lists of TAs, because multiple TAs can/must be assigned to some of the session occurrences (i.e., if they require more than one TA at a time). Example: `[{"TA_1", ["SO_1", "SO_2"]}]`
- `unused_tas`: List of TAs that were not assigned in the solution, i.e., all TAs that did not get at least one session occurrence to teach.
- `unused_session_occurrences`: List of session occurrences that did not get any TAs assigned.
- `lb`: The lower bound of the objective function.

### Solution evaluation

The objective function of the solution is calculated as follows:

- Let $S$ be the set of all session occurrences.
- Let $T(s)$ be the set of all TAs assigned to the session occurrence $s \in S$.
- Let $q(t, s)$ be the qualification of the TA $t$ for the session occurrence $s$.

minimize: $\sum_{s \in S}\sum_{t \in T(s)} q(t, s)$

The goal is to let the optimization choose the best matching TAs for every session occurrence.

### Solution feasibility

The solution feasibility depends on multiple constraints that must hold:

- Every session occurrence must have exactly the required number of TAs assigned. I.e., there must not be a session occurrence for which the number of assigned TAs is not equal to the required number of TAs.
- Every assigned TA must have at least a qualification $q > 0$ for the particular assigned session occurrence.
- The sum of all work hours assigned to a TA must not be larger than the maximum semester/yearly/time horizon work time of the TA.
- For every week in the planning horizon, the sum of the assigned work hours of a TA must not be larger than the maximum weekly work time of the TA.
- For every pair of assigned session occurrences for a TA, the time frame of those two session occurrences must not overlap. I.e., there are no two session a TA has to give that overlap at any point in time.
- A TA must not get a session occurrence assigned that takes place on a date this TA is blocked on.


## Instance data file

The problem instance file format can be structured in JSON (`.json`) format.
Here is a breakdown of each field:

- `name`: The name of the problem instance.
- `sessionOccurrences`: A list of all session occurrences of the problem. A single session occurrence has the following fields:
    - `name`: See problem instance description above.
    - `date_start`: See problem instance description above.
    - `date_end`: See problem instance description above.
    - `number_of_tas`: See problem instance description above.
    - `hours_paid_per_occurrence`: See problem instance description above.
    - `week`: See problem instance description above.
- `tas`: A list of all TAs of the problem. A single TA has the following fields:
    - `name`: See problem instance description above.
    - `qualifications`: Dictionary of key (name of the session occurrence) and value (qualification as number).
    - `max_hours_per_week`: See problem instance description above.
    - `max_hours_per_year`: See problem instance description above.
    - `blocked_dates`: See problem instance description above.

## Solution file

The solution file format can be structured in plain text (`.txt`) format or in JSON (`.json`) format.
Here is a breakdown of each field of the plain text-based representation:

- `NAME`: Name of the problem.
- `TYPE`: Type of the problem (`TA`).
- `#SessionOccurrences`: Number of session occurrences in the problem/solution.
- `#TeachingAssistants`: Number of TAs in the problem/solution.
- Mappings of session occurrences to TAs depicted by `->`
- Optional: Objective value as numeric value
- `EOF`

Here is a representation of the JSON representation:

- `name`: Name of the problem instance as described above.
- `sessionOccurrences`: List of session occurrences as described above.
- `tas`: List of TAs as described above.
- `mappings`: TA assignments in the for of a dictionary that maps session occurrence names to list of TA names.

## Example

### Instance

Here is an example of a problem instance file:

```json
{
    "name": "Teaching Assistant Assignment Problem Example",
    "sessionOccurrences": [
        {
            "name": "SO_A",
            "date_start": "2025-09-10 08:00:00",
            "date_end": "2025-09-10 10:00:00",
            "number_of_tas": 1,
            "hours_paid_per_occurrence": 2,
            "week": 1
        },
        {
            "name": "SO_B",
            "date_start": "2025-09-10 10:00:00",
            "date_end": "2025-09-10 12:00:00",
            "number_of_tas": 1,
            "hours_paid_per_occurrence": 2,
            "week": 1
        },{
            "name": "SO_C",
            "date_start": "2025-09-11 08:00:00",
            "date_end": "2025-09-11 10:00:00",
            "number_of_tas": 1,
            "hours_paid_per_occurrence": 2,
            "week": 1
        },{
            "name": "SO_D",
            "date_start": "2025-09-11 08:00:00",
            "date_end": "2025-09-11 10:00:00",
            "number_of_tas": 1,
            "hours_paid_per_occurrence": 2,
            "week": 1
        }
    ],
    "tas": [
        {
            "name": "TA_X",
            "qualifications": {
                "SO_C" : 2,
                "SO_D" : 2
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312
        },
        {
            "name": "TA_A",
            "qualifications": {
                "SO_A" : 1,
                "SO_B" : 2
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312
        },
        {
            "name": "TA_B",
            "qualifications": {
                "SO_A" : 2,
                "SO_B" : 1
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312
        },
        {
            "name": "TA_C",
            "qualifications": {
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312
        },
        {
            "name": "TA_D",
            "qualifications": {
                "SO_A" : 1,
                "SO_B" : 1
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312
        },
        {
            "name": "TA_E",
            "qualifications": {
                "SO_D" : 1
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312
        }
    ]
}
```

### Solution

Here is an example of a solution as plain text output:

```text
NAME : Teaching Assistant Assignment Problem Example
TYPE : TA
#SessionOccurrences : 4
#TeachingAssistants : 6
SO_A -> TA_B 
SO_B -> TA_A 
SO_C -> TA_X 
SO_D -> TA_E 
EOF
```

Here is an example of a solution as exported JSON file:

```json
{
    "name": "Teaching Assistant Assignment Problem Example",
    "sessionOccurrences": [
        {
            "name": "SO_A",
            "date_start": "2025-09-10 08:00:00",
            "date_end": "2025-09-10 10:00:00",
            "number_of_tas": 1,
            "hours_paid_per_occurrence": 2,
            "week": 1
        },
        {
            "name": "SO_B",
            "date_start": "2025-09-10 10:00:00",
            "date_end": "2025-09-10 12:00:00",
            "number_of_tas": 1,
            "hours_paid_per_occurrence": 2,
            "week": 1
        },
        {
            "name": "SO_C",
            "date_start": "2025-09-11 08:00:00",
            "date_end": "2025-09-11 10:00:00",
            "number_of_tas": 1,
            "hours_paid_per_occurrence": 2,
            "week": 1
        },
        {
            "name": "SO_D",
            "date_start": "2025-09-11 08:00:00",
            "date_end": "2025-09-11 10:00:00",
            "number_of_tas": 1,
            "hours_paid_per_occurrence": 2,
            "week": 1
        }
    ],
    "tas": [
        {
            "name": "TA_X",
            "qualifications": {
                "SO_C": 2,
                "SO_D": 2,
                "SO_A": 0,
                "SO_B": 0
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312,
            "blocked_dates": []
        },
        {
            "name": "TA_A",
            "qualifications": {
                "SO_A": 1,
                "SO_B": 2,
                "SO_C": 0,
                "SO_D": 0
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312,
            "blocked_dates": []
        },
        {
            "name": "TA_B",
            "qualifications": {
                "SO_A": 2,
                "SO_B": 1,
                "SO_C": 0,
                "SO_D": 0
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312,
            "blocked_dates": [
                "2025-09-10"
            ]
        },
        {
            "name": "TA_C",
            "qualifications": {
                "SO_A": 0,
                "SO_B": 0,
                "SO_C": 0,
                "SO_D": 0
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312,
            "blocked_dates": []
        },
        {
            "name": "TA_D",
            "qualifications": {
                "SO_A": 1,
                "SO_B": 1,
                "SO_C": 0,
                "SO_D": 0
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312,
            "blocked_dates": []
        },
        {
            "name": "TA_E",
            "qualifications": {
                "SO_D": 1,
                "SO_A": 0,
                "SO_B": 0,
                "SO_C": 0
            },
            "max_hours_per_week": 10,
            "max_hours_per_year": 312,
            "blocked_dates": []
        }
    ],
    "mappings": {
        "SO_B": [
            "TA_A"
        ],
        "SO_C": [
            "TA_X"
        ],
        "SO_A": [
            "TA_D"
        ],
        "SO_D": [
            "TA_E"
        ]
    }
}
```

The respective objective function value is: `-6`


### Explanation

- `TA_X` is the only TA that can give session `SO_C`.
- `TA_E` has the highest qualification for the session `SO_D`.
- `TA_C` has no qualifications at all, so they must not be assigned to any session.
- `TA_A`, `TA_B`, and `TA_D` can all potentially give the sessions `SO_A` and `SO_B`. However, `TA_B` is blocked for `2025-09-10` (on which `SO_A` and `SO_B` take place). `TA_A` is higher qualified for `SO_B`; as a result, `TA_A` gets assigned to `SO_B` and `TA_D` to `SO_A`.

The solution meets all constraints as explained above.

## Acknowledgements

This problem statement is based upon work from COST Action Randomised
Optimisation Algorithms Research Network (ROAR-NET), CA22137, is supported by
COST (European Cooperation in Science and Technology).

<!-- Please keep the above acknowledgement. Add any other acknowledgements as
relevant. -->

## References

X. Qu, W. Yi, T. Wang, S. Wang, L. Xiao, and Z. Liu, “Mixed-
integer linear programming models for teaching assistant assignment
and extensions,” Scientific Programming, vol. 2017, no. 1, pp. 1–7, 2017.
DOI: [10.1155/2017/9057947](https://doi.org/10.1155/2017/9057947) .
