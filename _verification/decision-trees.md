---
title: "Decision trees"
code: "V1063.001"
slug: "decision-trees"
technique: "Risk prioritization"
technique_id: "V1063"
technique_slug: "risk-prioritization"
tactic: "Threat modeling"
tactic_id: "VA09"
description: "SSVC decisions from exploitation, exposure and impact."
repos: 0
craft:
  - "Score each confirmed weakness on exploitation, exposure and impact."
  - "Map each combination to a fixed decision such as act now, act soon, track or defer."
  - "Store the decision tree in a file the team reviews each quarter."
reverse:
  - "An SSVC decision table or decision tree file in the repository."
  - "Triage labels such as act-now or defer on security issues."
  - "A reference to SSVC in the security policy."
packages:
  - id: "ssvc"
    name: "CERT/CC SSVC"
    url: "https://github.com/CERTCC/SSVC"
tools: []
examples: []
---
