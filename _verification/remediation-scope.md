---
title: "Remediation scope"
code: "V1047.003"
slug: "remediation-scope"
technique: "Scope and relevance filtering"
technique_id: "V1047"
technique_slug: "scope-and-relevance-filtering"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Check whether the fix stays inside the diff or reaches unchanged code."
repos: 0
craft:
  - "Check whether the suggested fix edits only lines inside the diff."
  - "Flag fixes that need changes to unchanged functions or callers as out of scope."
  - "Offer a follow-up issue instead of asking the author to widen the change."
reverse:
  - "Review comments that mark a suggested fix as touching code outside the diff."
  - "Follow-up issues titled with the file or function that a finding touches."
packages: []
tools: []
examples: []
---
