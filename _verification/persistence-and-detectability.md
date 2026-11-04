---
title: "Persistence and detectability"
code: "V1046.002"
slug: "persistence-and-detectability"
technique: "Severity scoring"
technique_id: "V1046"
technique_slug: "severity-scoring"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Transient, until restart or permanent; loud, silent or delayed."
repos: 0
craft:
  - "Record whether the defect is transient or persists until restart."
  - "Record whether the failure is loud, silent or delayed."
  - "Raise severity for silent or persistent failures in the scoring table."
reverse:
  - "A severity rubric that lists persistence and detectability levels."
  - "Finding records with separate persistence and detectability fields."
  - "Review comments that describe a silent or delayed failure."
packages: []
tools: []
examples: []
---
