<!--
SPDX-FileCopyrightText: 2025 Daniela Scherer dos Santos <dssantos@dei.uc.pt>

SPDX-License-Identifier: CC-BY-4.0 
-->


# Multiobjective Subgraph Problem

Daniela Scherer dos Santos and Luís Paquete, University of Coimbra, CISUC/LASI, DEI, Coimbra, Portugal  

Copyright 2025 Daniela Scherer dos Santos and Luís Paquete

This document is licensed under CC-BY-4.0.


## Introduction

Given a graph $G$, the **Multiobjective Subgraph (MOS)** problem [1] consists of finding the set of efficient subgraphs in $G$. A subgraph is considered efficient if there is no other feasible subgraph with at least as many edges and at most as many vertices, with at least one strict inequality.

The motivation for solving the MOS problem stems from its close relation to the Multiobjective Quasi-clique (MOQC) [1] problem, which can be effectively addressed through MOS. The MOQC seeks a quasi-clique with maximum density and number of vertices and has many real-world applications.



## Task

Given a graph, the goal is to identify a set of feasible subgraphs that approximates the set of efficient subgraphs as closely as possible. 

## Detailed description

Consider an undirected and simple graph $G = (V,E)$, where 
$V$ and $E$ are the vertex and edge sets of $G$, respectively. 
For a set of vertices $S \subseteq V$, we denote by $G_S=(S,E(S))$ the subgraph induced by $S$ in $G$.

Given $G$, 
the MOS problem asks for a subgraph $G_S$ induced by $S \subseteq V$ such that   

$$S \in \underset{S^\prime \subseteq V}{\arg\max}  \lbrace \left(|E(S^\prime|),  -|S^\prime| \right) \rbrace$$

Note that $G$ can be unconnected.


## Instance data file

Each instance file represents an **undirected simple graph** in a format commonly used for real-life graphs (e.g. Matrix Market '.mtx' files). Its structure is as follows:

#### Comments
- Lines starting with '%' are **comments**.
- They often contain metadata, descriptions, or source information about the graph.
- These lines should be ignored when reading the graph.

#### Header

The first non-comment line contains two integers:
- **First number:** Total number of vertices in the graph.
- **Second number:** Total number of edges in the graph. 

#### Edges
Each of the following lines represents an edge between two vertices. For example `1 2` indicates an edge between vertex 1 and vertex 2. Vertices are numbered consecutively from 1 to $|V|$.

## Solution file

The solution file describes the subgraph identified by the applied approach to solve the MOS problem. Its format is as follows:

- **First line:** An integer representing the number of vertices in the subgraph. 
- **Second line:** An integer representing the number of edges in subgraph.
- **Third line:** A list of vertex identifiers (integers) that belong to the subgraph. Each vertex should appear exactly once.

In case the approach for solving the problem returns a set of solutions, each solution should be reported in a single file.

## Example

### Instance

```
%%MatrixMarket matrix example
9 13
1 2
1 3
1 4
2 3
2 4
3 4
3 5
4 5
4 6
5 6
6 7
7 8
8 9
```
### Solution

```
5
7
1 2 3 4 6
```

### Explanation

The following figures illustrate the MOS problem for the example instance previously mentioned.

#### Original Graph G

This figure shows all vertices and edges in the input graph.

<img src="images/original.png" alt="Original Graph" width="300"/>

#### Feasible Solution

In the following figure, the subgraph induced by the green vertices corresponds to the **feasible solution** provided in the example. It contains 5 vertices and 7 edges.

<img src="images/feasible_MOS.png" alt="Feasible Solution" width="300"/>

Notice that the MOS problem does not impose any constraint on the connectedness of the solution subgraph. Therefore, a feasible subgraph can also be **unconnected**. 
The following figure shows such an example for the same input instance. It contains 5 vertices and 6 edges.

<img src="images/disconnected_MOS.png" alt="Disconnected Feasible Solution" width="300"/>


    
## Acknowledgements

This problem statement is based upon work from COST Action Randomised
Optimisation Algorithms Research Network (ROAR-NET), CA22137, is supported by
COST (European Cooperation in Science and Technology).


## References

[1] Daniela Scherer dos Santos, Kathrin Klamroth, Pedro Martins, and Luís Paquete.
2024. Solving the Multiobjective Quasi-clique Problem. European Journal of
Operational Research (2024). [https://doi.org/10.1016/j.ejor.2024.12.018](https://doi.org/10.1016/j.ejor.2024.12.018) 

