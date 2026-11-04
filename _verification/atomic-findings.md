---
title: "Atomic findings"
code: "V1042.004"
slug: "atomic-findings"
technique: "Evidence-backed verification"
technique_id: "V1042"
technique_slug: "evidence-backed-verification"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Split findings that make more than one claim so each is verified separately."
repos: 0
craft:
  - "Split any finding with more than one claim into separate findings."
  - "Verify each part on its own and record each verdict separately."
  - "Post a finding only when each of its parts is confirmed."
reverse:
  - "Review records with one verdict per claim rather than one per comment."
  - "Bot comments that carry a single claim each, with separate verdict lines."
packages: []
tools: []
examples: []
---
