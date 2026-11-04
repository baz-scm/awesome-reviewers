---
title: "Complexity limits"
code: "V1012"
slug: "complexity-limits"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Measures cyclomatic complexity, function length and nesting and fails when a change pushes a function past a limit."
subtechniques:
  - id: "V1012.001"
    name: "Complexity thresholds"
    slug: "complexity-thresholds"
    description: "Per-function limits on cyclomatic or cognitive complexity."
  - id: "V1012.002"
    name: "Size budgets"
    slug: "size-budgets"
    description: "Limits on function, file and parameter counts."
---
