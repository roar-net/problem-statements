# Optimal Scaling of Cloud Services

André Bento, University of Coimbra, Centre for Informatics and Systems of the University of Coimbra, Department of Informatics Engineering.

Copyright 2024 André Bento.

This document is licensed under CC-BY-4.0.

## Introduction

Cloud services operate on infrastructures that leverage shared resources, enabling these services to access the same physical resources independently. This model fosters scalability, flexibility, and cost-effectiveness for both providers and users of cloud services. Cloud services are encapsulated in containers, which can be replicated as necessary to maximize the utilization of infrastructure resources. This scalability ensures that the system can accommodate higher loads, thereby increasing availability for a given workload. As a result, each service dynamically utilizes a flexible allocation of vCPUs (Virtual Central Processing Units) and Gibibytes of Memory for every allocated replica. For instance, a login service may require 1 vCPU and 2 GiB of memory for each replica.
Among the crucial quality of service metrics are Availability and Cost. Availability represents the ratio of successful requests to total requests, while Cost encompasses the total expenses incurred across all replicas of all services.

## Task

The problem consists in determining the optimal replica configuration for the entire system, aiming at maximizing Availability (A) and minimizing Cost (C).

## Problem statement

The objective function is to minimize U + C, where U represents Unavailability (calculated as 1 - A), and C denotes the normalized cost of the entire system.
The first constraint aims at introducing a threshold for availability as a Service Level Objective (SLO) and is calculated as follows: A >= 1 - A_SLO.
The second constraint aims at introducing limits to the cost and is calculated as follows: 0 <= C <= 1.
The replica configuration for the entire system is represented by variable x. Each element x_i in x corresponds to the number of replicas for service i, where x_i is a positive integer value representing the number of replicas for service i.

A is computed by multiplying all the Availabilities of each service, A = A_1 * A_2 * ... * A_n.

C is computed by summing all the CPU and Memory requirements per replica.

## Instance data file

The problem instance file format can be structured in a plain text (txt) format.
Here is a breakdown of each field:

- NumberOfServices: Indicates the total number of services described in the file.
- A_SLO: Indicates the SLO for the Availability.
- ServiceName: Identifies the name or identifier of the service.
- Load: Represents the load on the service, measured in requests per second.
- CPURequirementPerReplica: Specifies the vCPU requirement per replica of the service.
- MemoryRequirementPerReplica: Specifies the memory requirement, in Gibibytes, per replica of the service.
- AmdhalP: Denotes the Amdahl's P value, which indicates the proportion of the task that can be parallelized.
- GLFA, GLFK, GLFC, GLFB, GLFV, GLFQ: These parameters relate to the Generalized Logistic Function (GLF), with each parameter representing a different coefficient or characteristic of the function (Availability function).
- CPUCostCoefficient, MemoryCostCoefficient: These coefficients likely represent the cost associated with CPU and memory usage, respectively.

Here is an example of a problem instance file:
```txt
NumberOfServices
A_SLO
1, ServiceName, Load, CPURequirementPerReplica, MemoryRequirementPerReplica, AmdhalP, GLFA, GLFK, GLFC, GLFB, GLFV, GLFQ
2, ServiceName, Load, CPURequirementPerReplica, MemoryRequirementPerReplica, AmdhalP, GLFA, GLFK, GLFC, GLFB, GLFV, GLFQ
...
CPUCostCoefficient,MemoryCostCoefficient
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
ObjectiveFunctionValue, Availability, Cost, Success
[Replica1, Replica2, ...]
```

## Example

### Instance

Here is an example of a problem instance file:
```txt
2
0.9
1, front-end, 1, 0.5, 1, 0.13447756374292408, 1.0286217700743516, 1.025725768730294, 0.9937672415588138, 0.00671433461475121, 0.0010703634023358406, 0.004259711742494379
2, catalogue, 1, 0.2, 0.2, 0.37523562442499, 1.4211722425198932, 0.9688699107930816, 1.501401141904585e-08, 0.02265990255071186, 16.092457989374267, 4.7297917338942606
0.0427,0.0039
```

### Solution

Here is an example of a problem solution file (possibly not the optimal global solution):
```txt
0.9871061228716791, 0.9525361228716791, 0.034570000000000004, True
[1, 1]
```

### Explanation

The solution of this example instance indicates that the optimal configuration for the system is to have one replica of the front-end service and one replica of the catalogue service. The value of the objective function is around 0.9871, with around 95.25% for the overall availability of the system, and the total cost is around 0.0346 $/hour. The solution meets all constraints.

### References

Bento, A., Araujo, F., & Barbosa, R. (2023). Cost-Availability Aware Scaling: Towards Optimal Scaling of Cloud Services. Journal of Grid Computing, 21(4), 80.
