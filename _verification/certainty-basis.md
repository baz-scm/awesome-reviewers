---
title: "Certainty basis"
code: "V1046.004"
slug: "certainty-basis"
technique: "Severity scoring"
technique_id: "V1046"
technique_slug: "severity-scoring"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Demonstrated by a run, traced in code, inferred from a name, or assumed."
repos: 0
craft:
  - "Record how each finding was checked: run, traced in code, inferred or assumed."
  - "Cap the severity of inferred or assumed findings below demonstrated ones."
  - "Ask the author for a run or trace before a finding is raised above its cap."
reverse:
  - "A certainty field in finding records with the values run, traced, inferred or assumed."
  - "Review comments that attach a reproduction or test run as evidence."
  - "A rubric that caps severity by certainty basis."
packages: []
tools: []
examples: []
---
