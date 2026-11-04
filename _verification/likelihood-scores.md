---
title: "Likelihood scores"
code: "V1063.002"
slug: "likelihood-scores"
technique: "Risk prioritization"
technique_id: "V1063"
technique_slug: "risk-prioritization"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "EPSS for known vulnerabilities."
repos: 0
craft:
  - "Look up the likelihood score for each known vulnerability from its identifier."
  - "Store the score next to the severity in the finding record."
  - "Refresh the scores on a fixed schedule and sort the queue by them."
reverse:
  - "Likelihood score fields next to severity in vulnerability records."
  - "A scheduled job that refreshes scores from a feed."
  - "A queue or report sorted by likelihood."
packages: []
tools: []
examples: []
---
