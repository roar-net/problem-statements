<!--
SPDX-FileCopyrightText: 2025 Michael Heider <michael.heider@uni-a.de>, Helena Segherr, Jonathan Wurth 

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

# LCS Solution Composition

Michael Heider, Universität Augsburg, Germany  
Helena Stegherr, Universität Augsburg, Germany  
Jonathatn Wurth, Universität Augsburg, Germany

<!-- Put two empty spaces at the end of each author line except the last for
proper formatting -->

Copyright 2025 the authors.

This document is licensed under CC-BY-4.0.

<!-- Complete the above accordingly. Copyright and licensing information must be
consistent with the comment at the beginning of the markdown file -->

## Introduction

Learning Classifier Systems (LCSs) are a type of evolutionary machine learning 
algorithm that constructs solutions to the learning task as a finite set of 
rules each approximating a share of the input space. Some LCSs separate the 
discovery of rules from the final composition of the model returned by the 
training process, e.g. SupRB https://doi.org/10.1145/3520304.3529014 or 
HEROS https://doi.org/10.1145/3712256.3726461. 

This problem statement describes the combinatorial optimization problem that
both systems have to solve to provide an accurate yet compact solution.

## Task

Describe the high-level optimisation task in one or two sentences.

## Detailed description

Provide a detailed description of the problem in this section. This should
detail what parameters characterise a problem instance, what characterises a
solution, how a solution is evaluated (e.g. an objective function), and solution
feasibility constraints.

## Instance data file

Describe the format of a problem instance file.

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
