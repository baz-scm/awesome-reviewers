---
title: "Counterevidence search"
code: "V1042.001"
slug: "counterevidence-search"
technique: "Evidence-backed verification"
technique_id: "V1042"
technique_slug: "evidence-backed-verification"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Look for guards, callers or tests that show the claimed failure cannot happen."
repos: 0
craft:
  - "Before posting a finding, search the code for guards, validation and callers that prevent the failure."
  - "Search the tests for cases that already cover the claimed input."
  - "Refute the finding and record the guard location when one is found."
reverse:
  - "Verdict records that cite a guard, check or test location for a refuted finding."
  - "Review tool output saying a finding was dismissed because of a guard in the code."
packages: []
tools: []
examples: []
---
