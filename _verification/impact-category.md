---
title: "Impact category"
code: "V1046.001"
slug: "impact-category"
technique: "Severity scoring"
technique_id: "V1046"
technique_slug: "severity-scoring"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Data loss, security, crash, wrong behaviour, performance, leak or maintainability."
repos: 0
craft:
  - "Pick one impact category from a fixed list for each finding."
  - "Use the list: data loss, security, crash, wrong behaviour, performance, leak or maintainability."
  - "Reject findings that name no impact category."
reverse:
  - "A severity rubric in review guidelines with an impact category list."
  - "Finding templates with a required impact field."
  - "Review comments that label a finding as a data loss or security issue."
packages: []
tools: []
examples: []
---
