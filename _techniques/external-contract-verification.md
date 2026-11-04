---
title: "External contract verification"
code: "V1044"
slug: "external-contract-verification"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Checks claims about third-party behaviour (an API can return null, a library throws) against authoritative documentation, and grades how strong that proof is."
subtechniques:
  - id: "V1044.001"
    name: "Documentation lookup"
    slug: "documentation-lookup"
    description: "Fetch the exact library version's documentation or source."
  - id: "V1044.002"
    name: "Proof grading"
    slug: "proof-grading"
    description: "Grade as definitive (spec or exhaustive enum), illustrative (an example) or unresolved."
---
