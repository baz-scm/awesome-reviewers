---
title: "Error-to-code mapping"
code: "V1064.001"
slug: "error-to-code-mapping"
technique: "Production error investigation"
technique_id: "V1064"
technique_slug: "production-error-investigation"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Map a stack trace or log pattern to the commit and lines responsible."
repos: 0
craft:
  - "Connect the agent read-only to logs, traces and the repository."
  - "Map each stack trace frame to the file, line and commit that introduced it."
  - "Report the commit that first produced the error pattern."
reverse:
  - "Observability integration config or runbook files in the repository."
  - "Incident notes that link an error signature to a commit or file."
  - "Stack trace fixtures used in tests of the mapping."
packages:
  - id: "holmesgpt"
    name: "HolmesGPT"
    url: "https://github.com/HolmesGPT/holmesgpt"
tools: []
examples: []
---
