---
title: "Complexity limits"
id: "V1012"
slug: "complexity-limits"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Measures cyclomatic complexity, function length and nesting and fails when a change pushes a function past a limit."
subtechniques:
  - id: "V1012.001"
    name: "Complexity thresholds"
    description: "Per-function limits on cyclomatic or cognitive complexity."
  - id: "V1012.002"
    name: "Size budgets"
    description: "Limits on function, file and parameter counts."
packages:
  - id: "radon"
    name: "Radon"
    url: "https://github.com/rubik/radon"
  - id: "lizard"
    name: "Lizard"
    url: "https://github.com/terryyin/lizard"
  - id: "ruff"
    name: "Ruff"
    url: "https://github.com/astral-sh/ruff"
craft:
  - "Measure the current distribution and set the limit at the existing worst case."
  - "Lower it over time; never block on files the change did not touch."
  - "Prefer a linter rule (ruff C901, ESLint complexity) over a separate tool."
reverse:
  - "max-complexity or complexity rules in linter config."
  - "radon or lizard reports in CI."
---
