---
title: "Symbolic execution"
id: "V1031"
slug: "symbolic-execution"
tactic: "Formal"
tactic_id: "VA05"
description: "Explores program paths with symbolic inputs and a solver to find inputs that violate an assertion."
subtechniques:
  - id: "V1031.001"
    name: "Bounded model checking"
    description: "Unroll loops to a bound and check all paths (CBMC)."
  - id: "V1031.002"
    name: "Contract checking"
    description: "Search for inputs that break a function's pre- and post-conditions (CrossHair)."
packages:
  - id: "cbmc"
    name: "CBMC"
    url: "https://github.com/diffblue/cbmc"
  - id: "klee"
    name: "KLEE"
    url: "https://github.com/klee/klee"
  - id: "crosshair"
    name: "CrossHair"
    url: "https://github.com/pschanely/CrossHair"
craft:
  - "Pick small pure functions with clear contracts."
  - "Write contracts as assertions or type annotations."
  - "Run with a time budget per function in CI."
reverse:
  - "CBMC harnesses, crosshair config or contract decorators in code."
---
