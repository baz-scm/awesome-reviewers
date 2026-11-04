---
title: "Code property graph queries"
code: "V1014.002"
slug: "code-property-graph-queries"
technique: "Data and control flow analysis"
technique_id: "V1014"
technique_slug: "data-and-control-flow-analysis"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Query syntax, control flow and data flow together to find custom bug patterns."
repos: 0
craft:
  - "Build a code property graph for the target language with Joern."
  - "Write a query that combines call, control and data flow for one bug pattern."
  - "Keep each query that found a real bug as a regression rule in the repository."
reverse:
  - "Joern query scripts (.sc files) committed to the repository."
  - "A CI job or make target that runs Joern queries against the build output."
  - "Test inputs that each saved query must flag and must not flag."
packages:
  - id: "joern"
    name: "Joern"
    url: "https://github.com/joernio/joern"
tools: []
examples: []
---
