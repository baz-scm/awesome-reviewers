---
title: "Symbolic execution"
code: "V1031"
slug: "symbolic-execution"
tactic: "Formal"
tactic_id: "VA05"
description: "Explores program paths with symbolic inputs and a solver to find inputs that violate an assertion."
subtechniques:
  - id: "V1031.001"
    name: "Bounded model checking"
    slug: "bounded-model-checking"
    description: "Unroll loops to a bound and check all paths (CBMC)."
  - id: "V1031.002"
    name: "Contract checking"
    slug: "contract-checking"
    description: "Search for inputs that break a function's pre- and post-conditions (CrossHair)."
---
