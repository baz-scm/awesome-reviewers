---
title: "Complexity thresholds"
code: "V1012.001"
slug: "complexity-thresholds"
technique: "Complexity limits"
technique_id: "V1012"
technique_slug: "complexity-limits"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Per-function limits on cyclomatic or cognitive complexity."
repos: 0
craft:
  - "Measure cyclomatic complexity of every function and record the current maximum."
  - "Set the limit at that maximum and fail only when a changed function exceeds it."
  - "Lower the limit in steps as functions are refactored."
reverse:
  - "A radon or lizard command in CI with a threshold argument."
  - "A max-complexity setting or a complexity rule in the linter config."
  - "A baseline file listing the functions that are above the limit."
packages:
  - id: "radon"
    name: "Radon"
    url: "https://github.com/rubik/radon"
  - id: "lizard"
    name: "Lizard"
    url: "https://github.com/terryyin/lizard"
tools: []
examples: []
---
