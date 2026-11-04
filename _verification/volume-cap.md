---
title: "Volume cap"
code: "V1048.001"
slug: "volume-cap"
technique: "Noise budget"
technique_id: "V1048"
technique_slug: "noise-budget"
tactic: "Finding validation"
tactic_id: "VA07"
description: "At most N comments per review, highest severity first."
repos: 0
craft:
  - "Set a maximum number of comments per review based on what reviewers act on."
  - "Sort candidate findings by severity, then by confidence."
  - "Post only the top findings up to the cap."
reverse:
  - "Review bot configuration with a maximum comment count or a per-review limit."
  - "A severity field on each finding and a sort step before posting."
packages: []
tools: []
examples: []
---
