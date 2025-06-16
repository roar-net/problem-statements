<!--
SPDX-FileCopyrightText: 2025 Francesca Da Ros <francesca.daros@uniud.it>

SPDX-License-Identifier: CC-BY-4.0
-->

# The Home Healthcare Routing and Scheduling Problem

Francesca Da Ros, Università degli Studi di Udine, Italy

Copyright 2025 Francesca Da Ros <francesca.daros@uniud.it>

This document is licensed under CC-BY-4.0.

## Introduction

Home Healthcare plays a crucial role in delivering medical and support
services directly to patients in their own homes. While this approach
is often more economical w.r.t. hospital care and can ease the
responsibilities placed on families, it also brings significant
logistical challenges - particularly in coordinating when and how
caregivers reach their patients.

The operational model of Home Healthcare involves specialized
caregivers visiting patients' homes to deliver required services
before proceeding to subsequent appointments. Therefore, unlike
traditional healthcare scheduling, these systems must account for both
the scheduling and routing of caregivers. This optimization problem,
known as the Home Healthcare Routing and Scheduling Problem (HHCRSP),
has emerged as a significant and complex issue within the Operations
Research community.

In this training project, we will deal with an extension of the HHCRSP
formulation proposed by Mankowska et al. [2]

## Task

The core objective of the HHCRSP is to determine, for each caregiver,
an optimal route and schedule for visiting patients. The optimization
aims to:

1. Minimize caregivers’ travel time
1. Minimize tardiness relative to patients’ availability windows
1. Minimize caregivers’ idle time
1. Minimize caregivers' overtime

## Detailed description

The HHCRSP involves scheduling caregiver visits to patients, where
each patient requires specialized services and specifies preferred
service times. The model optimizes daily scheduling decisions by
minimizing caregiver travel times between patient locations and
reducing deviations from patients' preferred time windows. Following,
the main characteristics of the problem are detailed. Additionally,
also possible extensions to the base problem formulation are reported
(You are not required to implement them, but if you have time and are
willing to, you can).

### Patients

They are the recipients of the services (at most two services), each
characterized by a set of attributes that may influence service
delivery planning. Each patient is associated with a specific
geographic position (i.e., their home), which is the destination for
caregivers' visits. The spatial distribution of patients, combined
with the underlying road and transportation networks, determines
travel times between locations.

The patients' temporal availability is represented by at least one
time window (in this basic formulation, each patient expresses one
time window, but ideally one can have multiple, see Extensions),
depending on personal schedules, preferences, or medical
requirements. Time windows establish constraints within which services
must be delivered.

### Services

They represent the specific care activities that must be delivered to
patients, spanning a broad spectrum of medical, therapeutic, and
supportive interventions. Each service is characterized by its nature
and purpose, ranging from clinical procedures such as medication
administration or wound care to supportive functions like personal
hygiene assistance or rehabilitation exercises. It is required the
appropriate matching of patient needs with caregiver capabilities.

Several parameters define the temporal dimension of services. Service
duration specifies the time required to complete the activity, which
may vary based on patient condition, service complexity, or caregiver
experience. Patients often require multiple services (at most two),
creating interdependencies that must be carefully
coordinated. Services may be subject to precedence relationships,
where certain activities must precede others to maintain care
continuity and effectiveness. The synchronization of services, mainly
when multiple caregivers must work in tandem, introduces additional
complexity to the scheduling problem.

### Caregivers

They are the workforce responsible for delivering services to
patients. Each caregiver has a unique professional profile defined by
their qualifications (also called specializations or
competencies). Qualifications are essential in planning, as not all
caregivers can perform all services.

Each caregiver typically operates within defined working time shifts,
establishing their availability throughout the planning horizon. These
shifts allow for overtime.

Mobility aspects further characterize caregivers within the
system. Each caregiver begins and ends their workday at designated
locations, which may be their home, a healthcare facility, or another
fixed point. Their movement between patient locations is governed by
available transportation modes, which influence travel times and
operational costs. In this formulation, we consider only one
transportation mode, i.e., individual cars.

### Planning horizon

In this formulation, we restrict the planning horizon to a single day
and time granularity based on minutes.

### Time windows

Patient availability is defined through time windows. Time window
enforcement is approached as follows: The service begins within the
designated time window, allowing the service to potentially extend
beyond the window's end.

### Services sync

When a patient require more than one service, the delivery pattern can
be one of the following. Services may be provided simultaneously, with
multiple caregivers attending to the patient at the same time; or
independently, allowing services to be scheduled without
interdependence.

### Incompatibilities 

The relationship between caregivers and patients extends beyond simple
service provision, including interpersonal dynamics that can impact
care quality and patient satisfaction. These relationships are
expressed in the form of incompatibilities. This will be then
accounted for in the objective function.

### Basic feasibility constraints

- All patients must be accounted for (i.e., all the required services
  must be provided).
- A service cannot be provided by a caregiver who is not qualified for
  it. This ensures that patients receive care only from caregivers
  with the appropriate skills and certifications required for their
  medical needs.
- A service cannot start before the patient's time window begins. In
  case of early arrival, the caregiver has to wait until the time
  window starts. This temporal constraint respects patient
  availability and preferences while ensuring service delivery occurs
  when patients are prepared to receive care.
- As soon as the service ends, the caregiver must depart from the
  patient location.

### Cost components

The objective function corresponds to the weighted sum of the
following components:

- **Travel time** represents the duration caregivers need to move
  between patient locations. It includes all movement within a
  caregiver's route, including travel from the starting location to
  the first patient, between consecutive patients, and from the final
  patient back to the ending location. This component directly
  influences operational costs through fuel consumption, vehicle wear,
  and productive time utilization. We consider the sum of all the
  travel times.
- **Tardiness** measures the delay in service delivery beyond the
  scheduled or promised time. This occur when a caregiver starts to
  deliver the service after the end of the time window. Tardiness
  negatively impacts patient satisfaction and may compromise care
  quality for time-sensitive services. We consider the sum of the
  tardiness w.r.t. all patients.
- **Idle time** represents the sum of all time periods within a
  caregiver's shift that are not used for patient service or
  travel. It is calculated as the total shift duration minus the
  combined service and travel time. Specifically, idle time includes
  three components: waiting time that occurs when a caregiver arrives
  early at a patient location; the time interval between shift start
  and departure to the first patient; and the period between returning
  to the ending location and the conclusion of the shift (only when
  this return occurs before the shift ends). This measure captures all
  non-productive periods within a caregiver's scheduled shift and
  represents potential inefficiency in resource utilization. We
  consider the maximum idle time.
- **Overtime** represents work performed beyond a caregiver's shift
  duration. It occurs when a caregiver's return time to their ending
  location exceeds their shift end time. This component typically
  incurs premium labor costs and may contribute to caregiver fatigue
  and decreased job satisfaction.
- **Waiting time** occurs when a caregiver arrives at a patient's
  location before their time window begins. During this period, the
  caregiver must wait until the earliest permissible service start
  time, resulting in unproductive time that nonetheless counts toward
  their work hours. This component represents inefficiency in schedule
  coordination between caregiver availability and patient time
  windows.
- **Incompatible caregivers** occurs when a patient is visited by a
  caregiver they is incompatible with.

The weights of the components are indicated in the instances metadata.

## Istance data file

The instance is encoded using a JSON format. Its core structure is as
follows:

```json
{
  "patients": [...],
  "caregivers": [...],
  "services": [...],
  "terminal_points": [...],
  "distances": [...],
  "metadata": {...},
}
```

Each patient in the "patients" list is represented by a unique
identifier and a set of attributes. The list of required services
("required_services"), where each item specifies the service and its
estimated duration -- this may differ from the default duration for
that service type (see below). Additionally, the patient's preferred
time windows for receiving care are recorded under the "time_windows"
field, where time is expressed in units (e.g., minutes) relative to
the beginning of the planning horizon. Finally, the patient's
geographical coordinates are provided along with the
"distance_matrix", which maps the location to an entry in the distance
matrix ("distances"). An example of patient declaration is ad follows:

```json
{
  "id": "p2",
  "required_services": [ { "service": "s3", "duration": 30 } ],
  "time_windows": [ { "start": 60, "end": 300 } ],
  "location": [ 13.3011, 38.1034 ], "distance_matrix_index": 4,
  "incompatible_caregiver":["c3"]
}
```

Each caregiver in the "caregivers" list is represented by a unique
identifier and a set of attributes.  The "abilities" field specifies
the services the caregiver is qualified to perform. The departure and
arrival points are identified by their respective indices, as defined
in the corresponding fields in the related section
"terminal_points". The "working_shift" field specifies the caregiver's
working hours. An example of caregiver declaration is ad follows:

```json
{
  "id": "c1",
  "abilities": [ "s3" ],
  "departing_point": "d1", "arrival_point": "d1",
  "working_shift": { "start": 0, "end": 600 }
}
```

An example of terminal point declaration is ad follows:

```json
{ "id": "d0", "distance_matrix_index": 0, "location": [ 13.3468, 38.1109 ] }
```

Each service in the "services" list is represented by a unique
identifier, its type, and a default duration (which may differ from
the duration required by a specific patient's needs). The distinction
between the identifier and its type allows for grouping related
services under broader categories. For example, under the type
"medical care", specific services such as "physiotherapy" or "wound
care" can be included, while the type ``daily activity'' may include
tasks like "bathing" or "house cleaning". The identifier is referenced
in the "required_services" list of patients and the "abilities" field
of caregivers. An example of service declaration is ad follows:

```json
{ "id": "s0", "type": "t0", "default_duration": 45 }
```

## Solution file

A solution to an HHCRSP instance consists of the following decisions:

1. The route each caregiver follows (i.e., the order in which patients
   are visited).
1. The arrival time, departure time, and service provided by each
   caregiver at each patient in their route.

The solution is encoded using a JSON format. Its core structure is as follows:

```json
{
   "routes": [...],
   "cost_components": {...},
   "cost": { "cost": ..., "violations": .. }
}
```

This format captures the routes ("routes"), along with optional fields
such as cost components and overall cost (both in terms of total cost
and the number of violations). While these additional fields are not
part of the solution itself, they facilitate comparability,
benchmarking, and debugging.

Each item in the "routes" list represents a caregiver and includes
their identifier ("caregiver_id") along with the list of locations
they visit ("locations"). Each location entry specifies the service
performed, the corresponding place (i.e., the patient), and the
temporal details of the visit (i.e., the start and end time of the
service are required). **Note that we assume that end_time ==
departure_time**. An example is as follows:

```json
{
  "caregiver_id": "c2",
  "locations": [
    ...
    { 
        "arrival_time": 430,  
        "start_time": 430,
        "end_time": 460,
        "departure_time": 460, 
        "patient": "p7", 
        "service": "s1" },
    ...
  ]
}
```

## Example

### Instance

This is instance i-1.json

```json
{
  "metadata": {
    "time_window_met": "at_service_start",
    "cost_components": {
      "travel_time": 1,
      "total_tardiness": 1,
      "max_idle_time": 1
    },
    "name": "school/instance-Cuneo-r_5-p_5-dp_5-apt_same_as_departure-h600-twm_at_service_start-rs_42-inc_0.0-opt_0.0-dtw_0.0-pcgr_0.0-sc_(2, 2)-sp_0.7",
    "origin": "generated",
    "horizon": 600,
    "generator_info": {
      "city": "Cuneo",
      "radius": 5.0,
      "patients": 5,
      "departing_points": 5,
      "arrival_points": 0,
      "arrival_point_type": "same_as_departure",
      "sync_rates": [
        0.7,
        0.2,
        0.1,
        0.0
      ],
      "incompatibility": 0.0,
      "service_classes": [
        2,
        2
      ],
      "optional_rate": 0.0,
      "double_time_window_rate": 0.0,
      "preferred_caregiver_rate": 0.0,
      "no_intersect_administrative": false,
      "patient_config": {
        "time_windows": [
          30,
          60,
          90,
          120
        ],
        "treatment_durations": [
          15,
          30,
          45,
          60
        ],
        "treatment_duration_biases": [
          0.1,
          0.35,
          0.35,
          0.2
        ],
        "sequential_distances": [
          0,
          15,
          30,
          45,
          60,
          75,
          90
        ],
        "time_window_granularity": 15
      },
      "caregiver_config": {
        "shift_durations": [
          600
        ],
        "shift_granularity": 30
      },
      "random_seed": 42
    }
  },
  "distances": [
    [
      0,
      17,
      17,
      8,
      11,
      11,
      11,
      17,
      8,
      12
    ],
    [
      17,
      0,
      2,
      13,
      11,
      11,
      12,
      0,
      13,
      7
    ],
    [
      18,
      2,
      0,
      16,
      13,
      13,
      13,
      2,
      16,
      9
    ],
    [
      9,
      14,
      15,
      0,
      10,
      10,
      11,
      14,
      0,
      8
    ],
    [
      11,
      12,
      13,
      10,
      0,
      0,
      4,
      12,
      10,
      10
    ],
    [
      11,
      12,
      13,
      10,
      0,
      0,
      4,
      12,
      10,
      10
    ],
    [
      11,
      12,
      13,
      11,
      4,
      4,
      0,
      12,
      11,
      10
    ],
    [
      17,
      0,
      2,
      13,
      11,
      11,
      12,
      0,
      13,
      7
    ],
    [
      9,
      14,
      15,
      0,
      10,
      10,
      11,
      14,
      0,
      8
    ],
    [
      12,
      7,
      9,
      8,
      10,
      10,
      10,
      7,
      8,
      0
    ]
  ],
  "terminal_points": [
    {
      "id": "d2",
      "distance_matrix_index": 2,
      "location": [
        7.584329474246332,
        44.489351042667934
      ]
    },
    {
      "id": "d1",
      "distance_matrix_index": 1,
      "location": [
        7.583945189196948,
        44.49836286907799
      ]
    },
    {
      "id": "d3",
      "distance_matrix_index": 3,
      "location": [
        7.509478682920628,
        44.478565744259285
      ]
    },
    {
      "id": "d0",
      "distance_matrix_index": 0,
      "location": [
        7.510665887443382,
        44.4515306913347
      ]
    },
    {
      "id": "d4",
      "distance_matrix_index": 4,
      "location": [
        7.536905586595426,
        44.42509160214148
      ]
    }
  ],
  "caregivers": [
    {
      "id": "c1",
      "abilities": [
        "s1"
      ],
      "departing_point": "d0",
      "arrival_point": "d0",
      "working_shift": {
        "start": 0,
        "end": 600
      }
    },
    {
      "id": "c2",
      "abilities": [
        "s3"
      ],
      "departing_point": "d1",
      "arrival_point": "d1",
      "working_shift": {
        "start": 0,
        "end": 600
      }
    },
    {
      "id": "c3",
      "abilities": [
        "s0",
        "s1"
      ],
      "departing_point": "d1",
      "arrival_point": "d1",
      "working_shift": {
        "start": 0,
        "end": 600
      }
    },
    {
      "id": "c4",
      "abilities": [
        "s2",
        "s3"
      ],
      "departing_point": "d3",
      "arrival_point": "d3",
      "working_shift": {
        "start": 0,
        "end": 600
      }
    }
  ],
  "patients": [
    {
      "id": "p0",
      "required_services": [
        {
          "service": "s1",
          "duration": 45
        }
      ],
      "distance_matrix_index": 5,
      "time_windows": [
        {
          "start": 105,
          "end": 345
        }
      ],
      "location": [
        7.536905586595426,
        44.42509160214148
      ]
    },
    {
      "id": "p1",
      "required_services": [
        {
          "service": "s0",
          "duration": 45
        }
      ],
      "distance_matrix_index": 6,
      "time_windows": [
        {
          "start": 345,
          "end": 465
        }
      ],
      "location": [
        7.54982170979869,
        44.416375441465874
      ]
    },
    {
      "id": "p2",
      "required_services": [
        {
          "service": "s2",
          "duration": 30
        }
      ],
      "distance_matrix_index": 7,
      "time_windows": [
        {
          "start": 45,
          "end": 225
        }
      ],
      "location": [
        7.583945189196948,
        44.49836286907799
      ]
    },
    {
      "id": "p3",
      "required_services": [
        {
          "service": "s0",
          "duration": 30
        }
      ],
      "distance_matrix_index": 8,
      "time_windows": [
        {
          "start": 300,
          "end": 480
        }
      ],
      "location": [
        7.509478682920628,
        44.478565744259285
      ]
    },
    {
      "id": "p4",
      "required_services": [
        {
          "service": "s3",
          "duration": 60
        },
        {
          "service": "s0",
          "duration": 30
        }
      ],
      "distance_matrix_index": 9,
      "time_windows": [
        {
          "start": 315,
          "end": 495
        }
      ],
      "location": [
        7.546705515708374,
        44.488470971940984
      ],
      "synchronization": {
        "type": "independent"
      }
    }
  ],
  "services": [
    {
      "id": "s0",
      "type": "t0",
      "default_duration": 30
    },
    {
      "id": "s1",
      "type": "t0",
      "default_duration": 45
    },
    {
      "id": "s2",
      "type": "t1",
      "default_duration": 30
    },
    {
      "id": "s3",
      "type": "t1",
      "default_duration": 60
    }
  ]
}
```

### Solution

This is a solution to instance i-1.json

```json
{
  "cost": {
    "objective": 644,
    "violations": 0
  },
  "cost_components": {
    "max_idle_time": 543,
    "total_tardiness": 0,
    "travel_time": 101
  },
  "global_ordering": [
    "p1",
    "p3",
    "p0",
    "p4",
    "p2"
  ],
  "routes": [
    {
      "caregiver_id": "c1",
      "locations": [
        {
          "arrival_time": 11,
          "departure_time": 150,
          "end_time": 150,
          "patient": "p0",
          "service": "s1",
          "start_time": 105
        }
      ]
    },
    {
      "caregiver_id": "c2",
      "locations": [
        {
          "arrival_time": 7,
          "departure_time": 375,
          "end_time": 375,
          "patient": "p4",
          "service": "s3",
          "start_time": 315
        }
      ]
    },
    {
      "caregiver_id": "c3",
      "locations": [
        {
          "arrival_time": 12,
          "departure_time": 390,
          "end_time": 390,
          "patient": "p1",
          "service": "s0",
          "start_time": 345
        },
        {
          "arrival_time": 401,
          "departure_time": 431,
          "end_time": 431,
          "patient": "p3",
          "service": "s0",
          "start_time": 401
        },
        {
          "arrival_time": 439,
          "departure_time": 469,
          "end_time": 469,
          "patient": "p4",
          "service": "s0",
          "start_time": 439
        }
      ]
    },
    {
      "caregiver_id": "c4",
      "locations": [
        {
          "arrival_time": 14,
          "departure_time": 75,
          "end_time": 75,
          "patient": "p2",
          "service": "s2",
          "start_time": 45
        }
      ]
    }
  ]
}
```

## Acknowledgements

This problem statement is based on the work by Ceschia et al. [1]
(part of the descriptions are taken from this journal article we
authored) and Mankowska et al. [2].

This problem statement is based upon work from COST Action Randomised
Optimisation Algorithms Research Network (ROAR-NET), CA22137, is
supported by COST (European Cooperation in Science and Technology).

## References

[1] Ceschia, Sara and Da Ros, Francesca and Di Gaspero, Luca and
Mancini, Simona and Maniezzo, Vittorio and Montemanni, Roberto and
Rosati, Roberto Maria and Schaerf, Andrea, "A Unified Formulation for
Home Healthcare Routing and Scheduling Problems", Submitted for
publication.

[2] Mankowska, Dorota Slawa and Meisel, Frank and Bierwirth,
Christian, "The home health care routing and scheduling problem with
interdependent services", _Health Care Management Science_, vol. 17,
no. 1, pp. 15-30, 2014.
[https://doi.org/10.1007/s10729-013-9243-1](https://doi.org/10.1007/s10729-013-9243-1).
