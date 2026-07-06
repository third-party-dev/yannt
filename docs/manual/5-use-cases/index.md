---
title: Use Cases
first-section-number: "5"
---

# Use Cases

TBD

<!-- <div class="none">

## Step-by-step task flows (CLI use cases)

 TODO

Each use case:

- A situation header: Its a header and its what users scan for.
  - Example: Does this model contain executable code?
- One-sentence setup
  - Must provide start condition
  - Must provide expected results
  - May filter out slightly different situations
- What are you looking at: Explain the results or output.

</div> -->

## Overview

Generally, I view use cases as functional requirements of a product (in contrast to non-functional requirements that are expressed in must/shall/should/may terminology). Those use case (requirements) then become the baseline for a test plan and subsequently lend themselves well to test procedures.

I do not intend for yannt to be that formal, but I would like to use the notion of use cases to meet the spirit of everything above, but in a more cohesive format. The idea is to describe an environment (similar to a test suite setup) and then follow through on a number of use cases that I intentionally support or plan to support. The use cases could be an intention to implement and describe the flow of the action, or they could be fully implemented features that includes commands to run with example outputs (based on the pre-defined environment).

There is a lot of cross over between different components of yannt and therefore I'm a bit undecided on the _best_ way to organize the documented use cases. For now, I am going to lean on the organization of the CLI interface as the ideal use case breakdown.

::: {.pagegroup}

### Table of Contents

- **5.2** - [Use cases for generating test data.](./5.2-test-usecases.md)
- **5.3** - [Use cases for parsing model files the _pparse_ way.](./5.3-pparse-usecases.md)
- **5.4** - [Use cases for analysis of model files.](./5.4-analysis-usecases.md)
- **5.5** - [Use cases for other yannt sub-commands.](./5.5-misc-usecases.md)
- **5.6** - [Use cases for parsing model files the _naive_ way.](./5.6-naive-usecases.md)

:::