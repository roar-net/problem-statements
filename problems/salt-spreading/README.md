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

<!-- Remove the section below before submitting -->

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

<!-- Remove the section above before submitting -->

# Problem Name – Salt Spreading

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

The case discussed here has been presented by the company Aiban that was
contracted to carry out the salt spreading task by the local authorities of the
Danish municipalities of Kerteminde and Middelfart.


## Task

<!--
Describe the high-level optimisation task in one or two sentences.
-->

Given a road network made of roads that need to be salted, roads that can be
transited and directions of transit, given a fleet of salt vehicles with a salt
capacity, ...  We want to find the set of routes that satisfy specific salting
requirements and minimizes to the total traveled distance. Minimizing the
traveled distance is correlated with achieving the task in the fastest way and
with the minimal environmental impact (CO2 imprint). In order to be usable in
practice the routes must take into account the capacity of the vehicle. If the
salt load is not enough the vehicle must visit a refill depot. Further, there
might be constraints on the shape of the routes to allow easy movements of the
vheicles. For example, U-turns in some parts of the networks are not allowed.

## Detailed description

<!--
Provide a detailed description of the problem in this section. This should
detail what parameters characterise a problem instance, what characterises a
solution, how a solution is evaluated (e.g. an objective function), and solution
feasibility constraints.
-->

A number of vehicles depart from their respective dwelling place nodes and have
to salt given set of roads. The load of salt that the vehicles can carry is in
general insufficient to cover all roads, therefore routes might include
reloading at opportune depots. After having salted the last requested road, the
vehicles always visit a depot where they are reloaded with fuell and salt before
heading to a dwelling place, ready for the next time. It is assumed that the
vehicles are "off duty" after the final reload, hence the path from the
refilling depot to their dwelling place does not count in the time duration and
in the cost calculation.  Further, due to the size of the vehicles and the
movements they have to make, U-turns at some intersections are not allowed.

<!--
The problem is a generalization of the Capacited Arcs Routing
Problem~\cite{Arc9} with the additional constraints of reloading and
U-turn avoidance.
-->

In the following we specify the problem more formally.

We represent the road network by a _mixed graph_ $\hat{G}=(V, E \cup \hat{A})$.
The set of nodes $V$ includes the set of road intersections, the set of
refilling depots $D$ and the set of dwelling places to the vehicles $H$. Each
vehicle has a single location $h$ from $H$ from which it departs and returns.
The set $E$ is the set of edges that can be traversed in both directions and it
includes the set $E_R$ of edges that are required to be salted.  The set of arcs
$A$ represents links that can be traversed only in one direction and it includes
the set $A_R$ of arcs required to be salted.

We call a \emph{trip} the sequence of arcs and edges visited by a vehicle
that depart from home or from a depot and arrive at home or at a
depot. A \emph{tour} is a sequence of trips that depart from home and
arrive at home.

We can denote by $Z$, indexed by $z$, the set of vehicles, by $K$, indexed by $k$,
the set of all trips and by $K^z \subseteq K$ the set of trips composing the route of the
vehicle $z \in Z$.

<!--
The mixed graph $\hat{G}$ can be transformed in a directed graph $G=(V,A)$ by substituting
every edge $(i,j) \in E$ by two antiparallel arcs $(i,j)$ and $(j,i)$
and keeping the required arcs, thus getting the sets ${A} =
A\cup\{(i,j),(j,i) : (i,j) \in E\}$ and $R = A_R\cup\{(i,j),(j,i): (i,j)
\in E_R\} \subseteq \hat{A}$.

Given a subset $S\subseteq V$, the cut set $\delta(S)$ denotes the set
of edges with exatly one endpoint in $S$; $\delta^+(S)$ is the set of
outgoing arcs and $\delta^-(S)$ the set of ingoing arcs.

Let $x^k_{ij}$ be a binary variable that indicates whether the link
$(i,j) \in E_R \cup A_R$ is served and let $y^k_{ij}\in \mathbb{Z}^+_0$ be
an integer variable representing the number of times a link $(i,j) \in
A$ is deadheaded.  Let $\alpha_{vk}$ and $\beta_{vk}$ for $v\in
D\cup H$ and $k\in K$ be auxiliary
binary variables that indicate whether a node is visited.
-->

We call a _trip_ the sequence of arcs and edges visited by a vehicle
that departs from a dwelling place or from a depot and arrives at a dwelling place or at a
depot. A _route_ is a sequence of trips that depart from a dwelling place and
arrives at a dwelling place.

The task is finding a set of routes of minimal total length such that:

- the required edges and required arcs are visited by at least one vehicle's route.
- the difference between the departure and the arrival time of each route is not greater than a given time limit $T$.
- At any point in the route the residual capacity is non-negative.


![gualandi](images/gualandi.pdf)

## Instance data file

Describe the format of a problem instance file.

The Data are provided by the company Aiban. It is in the form of a
spread sheet as seen in Figure~\ref{data}.

\begin{figure}

\centering

\includegraphics[width=\textwidth]{figs/data_excerpt}
\caption{}
\end{figure}

Each node ("Knude punkt") represents a road intersection and at each
node it is given a set of edges (roads) departing from that node. The
column ``status'' indicates whether an edge needs to be salted and in
which direction. A status of 1 indicates that the edges need to be
salted but the direction is free. A status of 2 indicates that the edge
must be salted in a predefined direction. A status of 3 indicates that
the edge does not need to be salted. We assume that all edges listed can
be traversed in both directions. {\mc{I need to ask to the company if
this is true.}

Each edge has a column indicating the length of the road ("l{\ae}ngde")
and a column indicating the breadth of the road ("salt m"), both
represented in meters. The vehicles are identical. They have a salt
capacity of $12.3 \mathrm{m}^3$ and they spread $30\textrm{ml}$ of salt
per $\mathrm{m}^2$ of road. Since, $1\textrm{ml} = 1
\mathrm{cm}^3=10^{-6}\mathrm{m^3}$, on each road segment of length $\ell$
and width $w$ (expressed in $\mathrm{m}$ they use $30\cdot 10^{-6} \cdot
\ell \cdot w\mathrm{m}^3$ of salt. The depots are in node 1 and in node 179
and the two drivers start and end at their dwelling places at node 2 and 130,
respectively. The salting of the roads has to be completed within 3.5
hours and the overall objective is to minimise the total travelled
distance. The drivers visit a depot before returning dwelling place with their
vehicles, therefore they start with a full cargo hold of salt and fuel
tanks. The path from the depot to dwelling place does not count in the traveling
time and distance.

## Solution file

Describe the format of a solution file.

## Example

### Instance

Provide a small example instance in the described format.

### Solution

Provide a feasible solution to the example instance in the described format
(including its evaluation measure).

### Explanation

Optionally, provide a descriptive and/or visual explanation of the solution (and
its evaluation measure value) for the instance.

## Acknowledgements

This problem statement is based upon work from COST Action Randomised
Optimisation Algorithms Research Network (ROAR-NET), CA22137, is supported by
COST (European Cooperation in Science and Technology).

<!-- Please keep the above acknowledgement. Add any other acknowledgements as
relevant. -->

## References

Put any relevant references here.
