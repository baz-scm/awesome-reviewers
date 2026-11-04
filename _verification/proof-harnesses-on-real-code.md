---
title: "Proof harnesses on real code"
code: "V1030.003"
slug: "proof-harnesses-on-real-code"
technique: "Proofs and specifications"
technique_id: "V1030"
technique_slug: "proofs-and-specifications"
tactic: "Formal"
tactic_id: "VA05"
description: "Bounded proofs over the production code itself (Kani)."
repos: 0
craft:
  - "Write a proof harness next to the production function, with symbolic inputs and assertions."
  - "Set the bounds for loops and input size and record them in the harness."
  - "Run the proof tool in CI on the crate or file that contains the harness."
reverse:
  - "#[kani::proof] functions in Rust source files."
  - "A cargo kani step in a workflow."
  - "CBMC harness files or Makefile targets that run cbmc on production sources."
packages:
  - id: "kani"
    name: "Kani"
    url: "https://github.com/model-checking/kani"
  - id: "cbmc"
    name: "CBMC"
    url: "https://github.com/diffblue/cbmc"
tools: []
examples: []
---
