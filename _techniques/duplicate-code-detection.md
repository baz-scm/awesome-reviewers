---
title: "Duplicate code detection"
code: "V1011"
slug: "duplicate-code-detection"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Finds copied blocks so a fix in one copy is not missed in the others, and flags new code that re-implements an existing helper."
subtechniques:
  - id: "V1011.001"
    name: "Token clone detection"
    slug: "token-clone-detection"
    description: "Report token-identical or near-identical blocks above a size threshold."
  - id: "V1011.002"
    name: "Semantic reuse check"
    slug: "semantic-reuse-check"
    description: "Search the codebase for an existing function that does what the new code does, by embedding or by name."
---
