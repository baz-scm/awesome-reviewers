---
title: "Live verification"
code: "V1008.003"
slug: "live-verification"
technique: "Secret scanning"
technique_id: "V1008"
technique_slug: "secret-scanning"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Test whether a found credential is still valid to prioritise rotation."
repos: 0
craft:
  - "Run trufflehog with verification enabled on the findings from a history scan."
  - "Mark each finding as live or inactive in the triage record."
  - "Rotate live credentials first and close inactive findings with a note."
reverse:
  - "A trufflehog CI step that runs with verification enabled."
  - "A triage log that marks each finding live or inactive."
  - "Rotation tickets ordered by verified status."
packages:
  - id: "trufflehog"
    name: "TruffleHog"
    url: "https://github.com/trufflesecurity/trufflehog"
tools: []
examples: []
---
