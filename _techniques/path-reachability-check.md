---
title: "Path reachability check"
code: "V1043"
slug: "path-reachability-check"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Decides whether the triggering state can reach the flagged line on this code path, given guards, early returns and types."
subtechniques:
  - id: "V1043.001"
    name: "Guard analysis"
    slug: "guard-analysis"
    description: "Find early returns, enclosing conditions and defaults that exclude the trigger."
  - id: "V1043.002"
    name: "Caller analysis"
    slug: "caller-analysis"
    description: "Find a real caller, config or workflow that produces the triggering state."
---
