#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: © 2025 Authors of the roar-net-api-py project <https://github.com/roar-net/roar-net-api-py/blob/main/AUTHORS>
#
# SPDX-License-Identifier: Apache-2.0

import datetime
from dateutil import parser

from ta import Solution
from ta_classes import SessionOccurrence
from ta_classes import TeachingAssistant


# ---------------------------------- Utilities --------------------------------

def date_str_to_epoch(date_str: str) -> float:
    """
    Converts a given date string to epoch time.
    """
    assert str is not None
    return parser.parse(date_str).timestamp()


def check_for_conflicting_assignment(solution: Solution, ta: TeachingAssistant, so: SessionOccurrence) -> bool:
    """
    Checks the given TA for possible assignment conflicts for the given session occurrence.
    """
    assert solution is not None
    assert ta is not None
    assert so is not None

    # For every found session occurrence, check if there is a conflict with the given session occurrence
    for assigned_so in get_all_assigned_sessions_of_ta(solution, ta):
        if check_two_occurrences_conflict(assigned_so, so):
            return True
    return False


def get_all_assigned_sessions_of_ta(solution: Solution, ta: TeachingAssistant) -> list[SessionOccurrence]:
    """
    Returns a list of all assigned session occurrences of the given TA.
    """
    assert solution is not None
    assert ta is not None

    # Find all assigned session occurrences
    assigned_sessions = []
    for so in solution.mapping.keys():
        if ta in solution.mapping[so]:
            for candidate_ta in solution.mapping[so]:
                if ta == candidate_ta:
                    assigned_sessions.append(so)

    return assigned_sessions


def check_two_occurrences_conflict(so_a: SessionOccurrence, so_b: SessionOccurrence) -> bool:
    """
    Returns True if the two given session occurrences have a time overlap.
    """
    assert so_a is not None
    assert so_b is not None

    # If the two session occurrences are the same, they overlap
    if so_a == so_b:
        return True

    # Convert the start and end dates to epochs ...
    epoch_a_start = date_str_to_epoch(so_a.date_start)
    epoch_a_end = date_str_to_epoch(so_a.date_end)
    epoch_b_start = date_str_to_epoch(so_b.date_start)
    epoch_b_end = date_str_to_epoch(so_b.date_end)
    # ... and check if the time frames overlap
    if epoch_a_start < epoch_b_end and epoch_a_end > epoch_b_start:
        return True
    return False


def check_occurrences_for_conflicts(sos: list[SessionOccurrence]) -> bool:
    """
    Checks each pair of session occurrences of a given list of session occurrences for time conflicts.
    If at least one conflict is found, the method returns True.
    """
    assert sos is not None

    for so_a in sos:
        for so_b in sos:
            if so_a != so_b:
                if check_two_occurrences_conflict(so_a, so_b):
                    return False
    return False


def get_work_time_of_ta_total(solution: Solution, ta: TeachingAssistant) -> int:
    """
    Extracts and returns the total work time for a given TA.
    """
    assert solution is not None
    assert ta is not None

    total_time = 0
    for so in get_all_assigned_sessions_of_ta(solution, ta):
        total_time += so.hours_paid_per_occurrence
    return total_time


def get_work_time_of_ta_in_week(solution: Solution, ta: TeachingAssistant, week: int) -> int:
    """
    Extracts and returns the work time for a given TA in a given week.
    """
    assert solution is not None
    assert ta is not None
    assert week is not None

    week_time = 0
    for so in get_all_assigned_sessions_of_ta(solution, ta):
        if so.week == week:
            week_time += so.hours_paid_per_occurrence
    return week_time


def is_ta_assignable_to_so(solution: Solution, ta: TeachingAssistant, so: SessionOccurrence) -> bool:
    """
    Returns True if a given TA can be assigned to the given session occurrence.
    """
    assert solution is not None
    assert ta is not None
    assert so is not None

    # The TA must not be assigned previously
    if ta not in solution.mapping[so]:
        # The TA must have some qualifications for the session occurrence
        if so in ta.qualifications and ta.qualifications[so] != 0:

            # The TA must also have enough time capacity available
            if so.hours_paid_per_occurrence + get_work_time_of_ta_total(solution,
                                                                        ta) <= ta.max_hours_per_year and so.hours_paid_per_occurrence + get_work_time_of_ta_in_week(
                    solution, ta, so.week) <= ta.max_hours_per_week:
                # The TA must not have a conflicting assignment
                if not check_for_conflicting_assignment(solution, ta, so):
                    return True
    return False


def is_ta_qualified_for_so(ta: TeachingAssistant, so: SessionOccurrence) -> bool:
    """
    Return True if a given TA has at least a qualification of < 0 for the given session occurrence.
    """
    assert ta is not None
    assert so is not None
    return so in ta.qualifications and ta.qualifications[so] < 0

def is_date_blocked(candidate: str, date: str) -> bool:
    """
    Returns True if the two given dates (candidate and date) overlap in year, month, and day.
    """
    assert candidate is not None
    assert date is not None

    # Remove trailing minutes, seconds, etc.
    candidate = candidate.split()[0]
    date = date.split()[0]

    candidate_date = datetime.datetime.strptime(candidate, "%Y-%m-%d").date()
    date_date = datetime.datetime.strptime(date, "%Y-%m-%d").date()
    if candidate_date.day == date_date.day and candidate_date.month == date_date.month and candidate_date.year == date_date.year:
        return True

    return False

def is_ta_bocked_in_so(ta: TeachingAssistant, so: SessionOccurrence) -> bool:
    """
    Returns True if the given TA is not blocked on the date of the given session occurrence.
    """
    assert ta is not None
    assert so is not None

    for blocked_date in ta.blocked_dates:
        if is_date_blocked(blocked_date, so.date_start):
            return True
        if is_date_blocked(blocked_date, so.date_end):
            return True
    return False
