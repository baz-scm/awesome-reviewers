---
title: "Contract checking"
code: "V1031.002"
slug: "contract-checking"
technique: "Symbolic execution"
technique_id: "V1031"
technique_slug: "symbolic-execution"
tactic: "Formal"
tactic_id: "VA05"
description: "Search for inputs that break a function's pre- and post-conditions (CrossHair)."
repos: 0
craft:
  - "Add type annotations and pre- and post-conditions to small pure functions."
  - "Run crosshair check on those modules with a time budget per function."
  - "Turn each counterexample into a unit test."
reverse:
  - "crosshair configuration or check commands in CI or the Makefile."
  - "Contract decorators or assert statements that state pre- and post-conditions."
  - "Test cases named after counterexamples found by the checker."
packages:
  - id: "crosshair"
    name: "CrossHair"
    url: "https://github.com/pschanely/CrossHair"
tools: []
examples: []
---
