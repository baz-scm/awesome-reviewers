---
title: "Path reachability check"
id: "V1043"
slug: "path-reachability-check"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Decides whether the triggering state can reach the flagged line on this code path, given guards, early returns and types."
subtechniques:
  - id: "V1043.001"
    name: "Guard analysis"
    description: "Find early returns, enclosing conditions and defaults that exclude the trigger."
  - id: "V1043.002"
    name: "Caller analysis"
    description: "Find a real caller, config or workflow that produces the triggering state."
packages:
  - id: "infer"
    name: "Infer"
    url: "https://github.com/meta/infer"
  - id: "joern"
    name: "Joern"
    url: "https://github.com/joernio/joern"
  - id: "scip"
    name: "SCIP"
    url: "https://github.com/scip-code/scip"
craft:
  - "For each finding, list the callers of the flagged function."
  - "Check each caller for guards that exclude the trigger."
  - "Mark findings with no established producer as unestablished, not confirmed."
reverse:
  - "Static analyzer configs with path-sensitive checks enabled."
---
