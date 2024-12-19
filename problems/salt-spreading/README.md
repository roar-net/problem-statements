<!--
SPDX-FileCopyrightText: 2024 Marco Chiarandini <marco@imada.sdu.dk>

SPDX-License-Identifier: CC-BY-SA-4.0
-->

<!-- Replace the comment above with your licence information for your problem
statement. Consider all copyright holders and contributors. -->

<!-- According to the copyright and licensing policy of ROAR-NET original
problem statements contributed to this repository shall be licensed under the
CC-BY-4.0 licence. In some cases CC-BY-SA-4.0 might be accepted, e.g., if the
problem is based upon an existing problem licensed under those terms. Please
provide a clear justification when opening the pull request if the problem is
not licensed under CC-BY-4.0 -->

<!-- Remove the section below before submitting 

# Problem template

This folder provides a template for problem statements.

Replace the problem statement below according to the instructions within that
file (and remove this section).

Place any images and figures in the `images` folder.

Place instance data in the `data` folder. The organisation within that folder is
merely a suggestion and may be adapted according to the problem needs.

Place any support material (e.g., instance generators, solution evaluators,
solution visualisers) in the `support` folder.

Template follows below.

---
-->

<!-- Remove the section above before submitting -->

# Salt Spreading

Marco Chiarandini, University of Southern Denmark, Denmark

<!-- Put two empty spaces at the end of each author line except the last for
proper formatting -->

Copyright 2024 Marco Chiarandini

This document is licensed under CC-BY-SA-4.0.

<!-- Complete the above accordingly. Copyright and licensing information must be
consistent with the comment at the beggining of the markdown file -->

## Introduction

<!--
In this section provide a brief introduction of the problem, possibly including
its motivation and context. This should be a short (2 or 3 paragraphs)
high-level description.
-->

In the winter season, when forecasts announce temperatures below the freezing
point, municipalities are faced with the task of spreading salt in their road
networks.

The problem described here was presented by Jens Kristian Fonnesbach owner of
the company [Aiban](https://aiban.dk/) and author of the book "[Spar Millioner
paa
Vintertjeneste](https://historia.dk/shop/13-business/90-fonnesbech-spar-millioner-paa-vintertjeneste-2017/)",
2017, Historia.  The data we will describe relate to salt spreading task for
which Aiban was contracted by local authorities of the Danish municipalities of
Kerteminde and Middelfart.

<div style="text-align:center;">
<img src="images/fonnesbech_cover.jpeg" alt="Book cover" style="max-width:70%;height:auto;">
</div>


## Task

<!--
Describe the high-level optimisation task in one or two sentences.
-->

Given a road network made of roads that need to be salted, roads that can be
transited and directions of transit, given a fleet of salt vehicles with a salt
capacity and refilling depots, we want to find the set of routes that satisfy
salting requirements and minimizes to the total traveled distance.  Minimizing
the traveled distance is correlated with accomplishing the salting task with the
least fuel consumption and thus minimal environmental impact (CO2 imprint). In
order to be usable in practice the routes must take into account the capacity of
the vehicle. If the salt load is not enough the vehicle must visit a refill
depot.  Further, there might be constraints on the shape of the routes to allow
easy movements of the vheicles. For example, U-turns in some parts of the
networks are not allowed.

## Detailed description

<!--
Provide a detailed description of the problem in this section. This should
detail what parameters characterise a problem instance, what characterises a
solution, how a solution is evaluated (e.g. an objective function), and solution
feasibility constraints.
-->

We are given a network of roads that can be traversed, among which some roads
must be salted. A number of vehicles depart from their respective dwelling place
nodes and have to salt the roads requesting it. The load of salt that the
vehicles can carry is in general insufficient to cover all roads, therefore
routes might include reloading at opportune depots. After having salted the last
requested road, the vehicles always visit a depot where they are reloaded with
fuell and salt before heading to a dwelling place, ready for the next time. It
is assumed that the vehicles are "off duty" after the final reload, hence the
path from the refilling depot to their dwelling place does not count in the time
duration and in the travling distance calculation.  Further, due to the size of
the vehicles and the movements they have to make, U-turns at some intersections
are not allowed.

<!--
The problem is a generalization of the Capacited Arcs Routing
Problem~\cite{Arc9} with the additional constraints of reloading and
U-turn avoidance.
-->

In the following we specify the problem more formally.

We represent the road network by a _mixed graph_ ${G}=(V, E \cup {A})$.  The set
of nodes $V$ includes the set of road intersections, the set of refilling
depots, $D$, and the set of dwelling places to the vehicles, $H$.  The set $E$
is the set of edges that can be traversed in both directions and it includes the
set $E_R$ of edges that must be salted (it is sufficient to salt them in only
one direction). The set of arcs $A$ represents links that can be traversed only
in one direction and it includes the set $A_R$ of arcs required to be salted.

We call _trip_ the sequence of edges and arcs visited by a vehicle that departs
from a dwelling place or from a depot and arrives at a dwelling place or at a
depot. A _route_ is a sequence of trips that departs from a dwelling place and
arrives at a dwelling place.

We denote by $Z$, indexed by $z$, the set of vehicles, by $K$, indexed by $k$,
the set of all trips and by $K_z \subseteq K$ the set of trips composing the
route of the vehicle $z \in Z$.  Each vehicle $z$ has a single dwelling location
$h_z$ from $H$ from which it departs and returns. Every depot has associated a
maximum refill load. After a vehicle has visited a depot we assume its load of
salt to be equal to the smallest between the capacity of the vehicle and the sum
of the maximum refill load of the depot with and of the residual load before the
visit.  

The task is finding a set of routes such that:

- edges in $E_R$ and arcs in $A_R$ are salted by at least one vehicle's route;
- the difference between the departure and the arrival time of each route is not
  greater than a given time limit $T$;
- at any point in the route the residual capacity of the vehicle is non-negative;
- there are no U-turns at nodes where they are not allowed;

and such that it minimizes the total length.

## Instance data file

<!--
Describe the format of a problem instance file.
-->

We provide two real-life instances and two examples. The real-life instances are
provided by the company Aiban and relate to the two Danish municipalities of
Kerteminde and Middelfart. We make available the original spreadsheet as well as
the post processed `json` format, which is going to be the standard format of
this problem statement.

See a description and details:

- [Kerteminde](data/kerteminde/description.md)
- [Middelfart](data/middelfart/description.md)

The `json` format contains an object for each of the following entities:

```json 
"required": [
    "name",
    "max_time",
    "nodes",
    "required": [
          "label",
          "position"
        ]
    "vehicles"
    "required": [
          "capacity",
          "home",
          "id"
        ]
    "depots",
    "required": [
          "label",
          "refill"
        ]
    "A",
     "required": [
          "arc",
          "len",
          "time"
        ]
    "A_R",
     "required": [
          "dem",
          "edge",
          "len",
          "time"
        ]
    "E_R",
     "required": [
          "dem",
          "edge",
          "len",
          "time"
        ]
    "U",
    "required": [
          "label"
        ]
  ]
```

Note that the instance does not contain an object for the edge set $E$ as every
edge in this set can be replaced by two arcs in opposite direction in the set
$A$.

The full [schema](support/schema.json) for validation of the `json` instances is
available in the `support` folder. See also a small example for the instance
[gualandi](data/gualandi/gualandi.json) described below.

## Solution file

<!-- Describe the format of a solution file. -->

In the solution file, routes beloning to different vehicles are written in
different rows. Each row lists the sequence of nodes to be visited. The route
starts at the dwelling node of the vehicle and ends at the last refilling depot.
Trips can be recognised by the visit to a refilling depot.

Example:

```text
2, 23, 24, 25, 24, 190, 23, 190, 189, 6, 7, 26, 79, 78, 82, 81, 80, 76, 74, 73, 71, 69, 68, 66, 58,
46, 44, 42, 43, 42, 44, 47, 48, 47, 57, 45, 46, 58, 66, 65, 66, 68, 70, 68, 70, 72, 75, 20, 19, 5, 17,
19, 17, 18, 16, 14, 12, 8, 10, 9, 10, 11, 13, 14, 13, 27, 28, 27, 29, 31, 101, 102, 101, 32, 33, 131,
132, 134, 106, 105, 104, 103, 35, 36, 191, 37, 38, 39, 40, 41, 110, 112, 115, 114, 115, 116, 117,
118, 125, 126, 128, 139, 140, 137, 138, 135, 136, 135, 132, 131, 133, 193, 103, 104, 38, 37, 36,
35, 34, 30, 29, 30, 32, 101, 31, 99, 100, 294
130, 128, 126, 124, 117, 116, 120, 122, 123, 122, 120, 119, 121, 119, 118, 125, 127, 129, 127,
166, 164, 167, 170, 168, 170, 171, 169, 171, 173, 172, 173, 175, 174, 175, 177, 176, 177, 179,
178, 179, 181, 182, 180, 182, 184, 183, 184, 186, 188, 187, 157, 142, 157, 156, 158, 159, 158,
185, 187, 143, 144, 188, 186, 185, 158, 156, 194, 155, 194, 154, 160, 162, 160, 152, 153, 154,
153, 148, 151, 149, 151, 152, 160, 161, 181, 161, 163, 164, 163, 150, 163, 164, 167, 164, 166,
147, 130, 141, 146, 145, 146, 147, 146, 141, 140, 139, 134, 133, 193, 105, 106, 107, 39, 107,
108, 124, 108, 109, 111, 112, 113, 112, 115, 111, 109, 41, 40, 45, 57, 59, 58, 59, 64, 61, 65, 67,
62, 61, 64, 60, 54, 52, 53, 52, 51, 50, 192, 51, 50, 48, 49, 48, 47, 46, 44, 46, 47, 57, 55, 56, 55,
54, 60, 62, 63, 62, 67, 69, 71, 74, 73, 72, 75, 20, 21, 22, 21, 4, 3, 2, 1, 1, 2, 3, 189, 6, 5, 4,
5, 19, 20, 19, 16, 18, 15, 17, 15, 12, 11, 9, 8, 7, 26, 79, 85, 84, 82, 78, 77, 76, 77, 80, 81, 83, 89,
92, 93, 92, 91, 89, 83, 88, 90, 94, 95, 87, 90, 94, 97, 96, 86, 85, 84, 87, 86, 96, 95, 94, 97, 98, 294
```

## Example

### Instance

<!-- Provide a small example instance in the described format. -->

There are two small instances that can be used as examples.

<!--
![gualandi](images/gualandi.png){ width="515" height="385" style="display:
block; margin: 0 auto; text-align: center" }
-->


<div style="text-align: center;">
<img src="data/belben/map.png" alt="Belenguer Benavent instance">
</div>

<div style="text-align: center;">
<img src="data/gualandi/map.png" alt="Gualandi instance">
</div>


### Solution
<!--
Provide a feasible solution to the example instance in the described format
(including its evaluation measure).
-->

To be added


### Explanation

<!-- Optionally, provide a --> 

Descriptive and/or visual explanation of the solution (and
its evaluation measure value) for the instance.

## Acknowledgements

This problem statement is based upon work from COST Action Randomised
Optimisation Algorithms Research Network (ROAR-NET), CA22137, is supported by
COST (European Cooperation in Science and Technology).

<!-- Please keep the above acknowledgement. Add any other acknowledgements as
relevant. -->

## References

- Jens Kristian Fonnesbach, "[Spar Millioner paa
  Vintertjeneste](https://historia.dk/shop/13-business/90-fonnesbech-spar-millioner-paa-vintertjeneste-2017/)",
  2017, Historia. 

- Belenguer, José M.; Benavent, Enrique "A cutting plane algorithm for the
  capacitated arc routing problem" Computers & operations research , 04/2003,
  Volume 30, Issue 5
