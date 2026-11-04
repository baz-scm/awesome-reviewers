---
title: "Coverage check"
code: "V1061.002"
slug: "coverage-check"
technique: "Mitigation mapping"
technique_id: "V1061"
technique_slug: "mitigation-mapping"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "Report entry points that bypass the controls."
repos: 0
craft:
  - "Route each entry point through the inventory of controls."
  - "List entry points that skip every control in the inventory."
  - "Report only weaknesses at entry points with no control in front of them."
reverse:
  - "A coverage report or CI output that lists entry points without a control."
  - "Route definitions that show control middleware applied to each group."
  - "Exemption entries with a reason for each entry point that skips a control."
packages: []
tools: []
examples: []
---
