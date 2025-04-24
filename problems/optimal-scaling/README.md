# Optimal Scaling of Cloud Services

André Bento, University of Coimbra, Centre for Informatics and Systems of the University of Coimbra, Department of Informatics Engineering.

Copyright 2024 André Bento.

This document is licensed under CC-BY-4.0.

## Introduction

Cloud services operate on infrastructures that leverage shared resources, enabling these services to access the same physical resources independently. This model fosters scalability, flexibility, and cost-effectiveness for both providers and users of cloud services. Cloud services are encapsulated in containers, which can be replicated as necessary to maximize the utilization of infrastructure resources. This scalability ensures that the system can accommodate higher loads, thereby increasing availability for a given workload. As a result, each service dynamically utilizes a flexible allocation of Virtual Central Processing Units (vCPUs) and Gibibytes of Memory for every allocated replica. For instance, a login service may require 1 vCPU and 2 GiB of memory for each replica.
Among the crucial quality of service metrics are Availability and Cost. Availability represents the ratio of successful requests to total requests, while Cost encompasses the total expenses incurred across all replicas of all services.

## Task

The problem consists in determining the optimal replica configuration for the entire system, aiming at maximizing Availability ($A$) and minimizing Cost ($C$).

## Problem statement

The objective function is to minimize $U + C$, where $U$ represents Unavailability (calculated as $1 - A$), and $C$ denotes the normalized cost of the entire system.
The first constraint aims at introducing a threshold for availability as a Service Level Objective (SLO) and is calculated as follows: $A >= 1 - A_{SLO}$.
The second constraint aims at introducing limits to the cost and is calculated as follows: $0 <= C <= 1$.
The replica configuration for the entire system is represented by variable $x$. Each element $x_i$ in $x$ corresponds to the number of replicas for service $i$, where $x_i$ is a positive integer value representing the number of replicas for service $i$.

$A$ is computed by multiplying all the Availabilities of each service, $A = A_1 * A_2 * ... * A_n$.

$C$ is computed by summing all the CPU and Memory requirements per replica, $C = \frac{\sum_{i=1}^{n}\sum_{j=1}^{r}{\left(c_c \times \textit{cpu}_{i} + c_m \times \textit{mem}_{i}\right) \times x_{ij}}}{C_{max}}$.

## Instance data file

The problem instance file format can be structured in a plain text (txt) format.
Here is a breakdown of each field:

- NSvcs: Indicates the total number of services described in the file.
- ASLO: Indicates the SLO for the Availability.
- SvcId: Identifies the service, starting from 1.
- Load: Represents the load on the service, measured in requests per second.
- CPUPerReplica: Specifies the vCPU requirement per replica of the service.
- MemPerReplica: Specifies the memory requirement, in Gibibytes, per replica of the service.
- CPUCostCoeff, MemCostCoeff: These coefficients represent the cost associated with CPU and memory usage, respectively.

Here is an example of a problem instance file:
```txt
NSvcs
ASLO
SvcId1, Load, CPUPerReplica, MemPerReplica
SvcId2, Load, CPUPerReplica, MemPerReplica
...
CPUCostCoeff,MemCostCoeff
```

## Solution file

The problem instance file format can be structured in a plain text (txt) format.
Here is a breakdown of each field:

- ObjectiveFunctionValue: The value of the objective function of the solution.
- Availability: The overall availability of the system.
- Cost: The total cost of the solution.
- Success: A flag indicating whether the solution meets all constraints.
- [Replica1, Replica2, ...]: An array listing the replicas for each service, x, representing the optimal configuration of the system.

Here is an example of a problem solution file:
```txt
ObjFuncVal, A, C
[RplSvc1, RplSvc2, ...]
```

## Example

### Instance

Here is an example of a problem instance file:
```txt
2
0.9
1, 1, 0.5, 1
2, 1, 0.2, 0.2
0.0427,0.0039
```

### Solution

Here is an example of a problem solution file (possibly not the optimal global solution):
```txt
0.9871061228716791, 0.9525361228716791, 0.034570000000000004
[1, 1]
```

### Explanation

The solution of this example instance indicates that the optimal configuration for the system is to have one replica of the service 1 and one replica of the service 2. The value of the objective function is around 0.9871, with around 95.25% for the overall availability of the system, and the total cost is around 0.0346 $/hour. The solution meets all constraints.

## Acknowledgements

This problem statement is based upon work from COST Action Randomised Optimisation Algorithms Research Network (ROAR-NET), CA22137, is supported by COST (European Cooperation in Science and Technology), and is also funded in part by the Portuguese Foundation for Science and Technology (FCT) through Doctoral Grant No. BD.06012.2021.

### References

Bento, A., Araujo, F., & Barbosa, R. (2023). Cost-Availability Aware Scaling: Towards Optimal Scaling of Cloud Services. Journal of Grid Computing, 21(4), 80.
