---
title: "Caller analysis"
code: "V1043.002"
slug: "caller-analysis"
technique: "Path reachability check"
technique_id: "V1043"
technique_slug: "path-reachability-check"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Find a real caller, config or workflow that produces the triggering state."
repos: 0
craft:
  - "List every caller of the flagged function with a symbol index or call graph."
  - "Check each caller for the config, route or job that passes the triggering value."
  - "Mark the finding unestablished when no caller produces the state."
reverse:
  - "An index.scip file or a scip indexing step in CI."
  - "A joern call graph export or script in the repository."
  - "Finding records that name the caller or config that produces the state."
packages:
  - id: "scip"
    name: "SCIP"
    url: "https://github.com/scip-code/scip"
  - id: "joern"
    name: "Joern"
    url: "https://github.com/joernio/joern"
tools: []
examples: []
---
