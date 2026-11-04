---
title: "Bounded model checking"
code: "V1031.001"
slug: "bounded-model-checking"
technique: "Symbolic execution"
technique_id: "V1031"
technique_slug: "symbolic-execution"
tactic: "Formal"
tactic_id: "VA05"
description: "Unroll loops to a bound and check all paths (CBMC)."
repos: 0
craft:
  - "Write a harness that sets the inputs of one function to nondeterministic values."
  - "Set an unwinding bound for each loop and check that the bound is reached."
  - "Run the checker in CI with a time limit per harness."
reverse:
  - "CBMC harness files or Kani proof functions in the source tree."
  - "CI steps that invoke cbmc or cargo kani."
  - "unwind or unwinding settings in harness or config files."
packages:
  - id: "cbmc"
    name: "CBMC"
    url: "https://github.com/diffblue/cbmc"
  - id: "kani"
    name: "Kani"
    url: "https://github.com/model-checking/kani"
tools: []
examples: []
---
