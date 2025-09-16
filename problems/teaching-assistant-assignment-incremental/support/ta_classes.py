#!/usr/bin/env python3
#
# SPDX-FileCopyrightText: © 2025 Authors of the roar-net-api-py project <https://github.com/roar-net/roar-net-api-py/blob/main/AUTHORS>
#
# SPDX-License-Identifier: Apache-2.0

# ---------------------------------- Data classes --------------------------------

class SessionOccurrence:
    """
    Represents a session occurrence of the TA problem.
    """

    def __init__(self, name: str, date_start: str, date_end: str, number_of_tas: int, hours_paid_per_occurrence: int,
                 week: int):
        assert name is not None
        assert date_start is not None
        assert date_end is not None
        assert number_of_tas is not None and number_of_tas >= 1
        assert hours_paid_per_occurrence is not None and hours_paid_per_occurrence >= 1
        assert week is not None and week >= 0

        self.name = name
        self.date_start = date_start
        self.date_end = date_end
        self.number_of_tas = number_of_tas
        self.hours_paid_per_occurrence = hours_paid_per_occurrence
        self.week = week

    def __repr__(self):
        return self.name

    # def __eq__(self, other):
    #     if not isinstance(other, SessionOccurrence):
    #         return NotImplemented
    #     return self.name == other.name


class TeachingAssistant:
    """
    Represents a Teaching Assistant (TA) of the TA problem.
    """

    def __init__(self, name: str, qualifications: dict[SessionOccurrence, int], max_hours_per_week: int,
                 max_hours_per_year: int, blocked_dates: list[str]):
        assert name is not None
        assert qualifications is not None
        assert max_hours_per_week is not None and max_hours_per_week >= 0
        assert max_hours_per_year is not None and max_hours_per_year >= 0
        assert blocked_dates is not None

        self.name = name
        self.qualifications = qualifications
        self.max_hours_per_week = max_hours_per_week
        self.max_hours_per_year = max_hours_per_year
        self.blocked_dates = blocked_dates

    def __repr__(self):
        # return "Teaching Assistant: ".join(self.name) #+ ": qualifications: ".join(self.qualifications)
        # TODO: add qualifications to the method as well
        return self.name

    # def __eq__(self, other):
    #     if not isinstance(other, TeachingAssistant):
    #         return NotImplemented
    #     return self.name == other.name
