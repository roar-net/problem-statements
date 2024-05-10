<!--
SPDX-FileCopyrightText: 2024 Alexandre Jesus <me@adbjesus.com>

SPDX-License-Identifier: CC-BY-4.0
-->

# Contributing

We are glad that you want to contribute to our problem statements
repository. This document will try to answer some common questions that may
arise.

## Issues

We use GitHub to track and discuss all project issues. If you identify any kind
of issue or bug in the project (for example a mistake in a problem statement or
bug in some code), or have ideas for improvements please feel free to open a new
issue [here](https://github.com/roar-net/problem-statements/issues).

## Contributions

We follow a [forking
workflow](https://docs.github.com/en/get-started/exploring-projects-on-github/contributing-to-a-project)
for contributions to this repository. The main steps are:

1. Fork the project (https://github.com/roar-net/problem-statements/fork)
1. Create a feature branch
1. Stage, commit, and push your changes
1. Create a [Pull Request](https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests)

After you create a pull request the maintainers of this repository will review
it to validate its correctness and relevance. Any issues identified will be
discussed in the pull request discussion.

### Problem submission

To submit a problem statement open a pull request with a new problem inside the
`problems` folder following the template provided in
[templates/problem](./templates/problem).

Each problem must have its own folder inside the `problems` folder. The name of
the folder should be in kebab-case and sufficiently descriptive, e.g.,
`binary-knapsack` for the 0-1 Knapsack Problem, or `tsp` for the Traveling
Salesman Problem.

### Continuous Integration

When you create a pull request several checks are automatically performed, in
particular:

- We run the [REUSE Tool](https://github.com/fsfe/reuse-tool/) to make sure that
  has copyright and licensing information (see below)
- We run [mdl](https://github.com/markdownlint/markdownlint) to make sure all
  markdown files (if there are any) are correctly formatted.

In order to have your contribution accepted into the repository both checks
should pass successfully.

We provide a pre-commit config that automatically runs these checks locally
before you commit your changes.

### Copyright and Licensing

Every file should be licensed to avoid any ambiguity on reuse. We follow the
[REUSE Specification - Version 3.0](https://reuse.software/spec/) to declare
copyright and licence information for all files in a standardised
way. Furthremore, we use the [REUSE Tool](https://github.com/fsfe/reuse-tool/)
to automatically check that all files have the required copyright and licence
information.

Note that this repository is governed under the Copyright and Licensing Policy
of ROAR-NET which can be found [here](https://roar-net.eu/copyright_policy). In
particular, original problem statements and support materials are expected to be
licensed under the CC-BY-4.0 or Apache 2.0 licences as appropriate. Exceptions
for non-original or derivative work shall be analysed on a case-by-case basis
taking into account the goals of the COST Action. One general exception in this
repository is that sample data files may be licensed under CC0-1.0 if you wish
for ease of use. Contributions not abiding to this policy may be rejected.
