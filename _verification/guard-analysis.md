---
title: "Guard analysis"
code: "V1043.001"
slug: "guard-analysis"
technique: "Path reachability check"
technique_id: "V1043"
technique_slug: "path-reachability-check"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Find early returns, enclosing conditions and defaults that exclude the trigger."
repos: 0
craft:
  - "Run a path-sensitive analyzer on the flagged function."
  - "Read the early returns, enclosing conditions and default values on the path to the flagged line."
  - "Mark a finding as excluded when a guard blocks the trigger, and cite the guard's line."
reverse:
  - "An infer run in CI or an infer configuration file."
  - "A joern query script that walks control flow to a sink."
  - "Suppression entries that cite the guard line that excludes the finding."
packages:
  - id: "infer"
    name: "Infer"
    url: "https://github.com/meta/infer"
  - id: "joern"
    name: "Joern"
    url: "https://github.com/joernio/joern"
tools: []
examples: []
---
