---
title: "Intent scoping"
code: "V1047.002"
slug: "intent-scoping"
technique: "Scope and relevance filtering"
technique_id: "V1047"
technique_slug: "scope-and-relevance-filtering"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Move findings outside the PR's intent to follow-up work."
repos: 0
craft:
  - "Compare each finding against the pull request title and linked ticket."
  - "Move findings outside the stated intent into a separate issue."
  - "Tell the author in the review that the issue exists, so the finding is not silently dropped."
reverse:
  - "Issues created from review findings and linked back to the pull request."
  - "A pull request template that asks for the intent or a linked ticket."
packages: []
tools: []
examples: []
---
