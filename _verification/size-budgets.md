---
title: "Size budgets"
code: "V1012.002"
slug: "size-budgets"
technique: "Complexity limits"
technique_id: "V1012"
technique_slug: "complexity-limits"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Limits on function, file and parameter counts."
repos: 0
craft:
  - "Choose limits for function length, file length and parameter count from the current distribution."
  - "Fail the check only on functions and files that the change touched."
  - "Tighten each limit once the worst existing case has been reduced."
reverse:
  - "A lizard run in CI with length or argument limits."
  - "A linter setting for max-args or max-statements in the config."
  - "A baseline file that lists the existing oversized functions."
packages:
  - id: "lizard"
    name: "Lizard"
    url: "https://github.com/terryyin/lizard"
tools: []
examples: []
---
