---
title: "Call graph impact"
code: "V1014.003"
slug: "call-graph-impact"
technique: "Data and control flow analysis"
technique_id: "V1014"
technique_slug: "data-and-control-flow-analysis"
tactic: "Static analysis"
tactic_id: "VA02"
description: "List every caller and downstream consumer of a changed symbol."
repos: 0
craft:
  - "Generate a SCIP index for the repository on each default-branch build."
  - "Look up every reference to a changed symbol in the index."
  - "List the callers and downstream consumers in the review comment for the change."
reverse:
  - "A SCIP indexer step or index.scip artifact uploaded in CI."
  - "Code navigation links that resolve references across packages."
  - "A review note that lists callers of a changed function."
packages:
  - id: "scip"
    name: "SCIP"
    url: "https://github.com/scip-code/scip"
tools: []
examples: []
---
