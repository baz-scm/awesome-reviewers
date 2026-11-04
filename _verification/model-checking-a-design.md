---
title: "Model checking a design"
code: "V1030.001"
slug: "model-checking-a-design"
technique: "Proofs and specifications"
technique_id: "V1030"
technique_slug: "proofs-and-specifications"
tactic: "Formal"
tactic_id: "VA05"
description: "Write a TLA+ spec and check invariants over all reachable states."
repos: 1
craft:
  - "Write a spec for the part where a bug would be costly, such as commit or leader election logic."
  - "State the safety invariants and check them over all reachable states with the TLA+ tools."
  - "Run the checker in CI on every change to the spec file."
reverse:
  - "*.tla spec files with matching .cfg configuration files."
  - "A CI job that runs the TLA+ tools on the spec."
  - "Comments in the code that name the spec action they implement."
packages:
  - id: "tlaplus"
    name: "TLA+ tools"
    url: "https://github.com/tlaplus/tlaplus"
tools:
  - name: "tla-plus"
    repos: 1
examples: []
---
