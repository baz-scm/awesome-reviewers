---
title: "Spelling"
code: "V1003"
slug: "spelling"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Finds misspellings in identifiers, comments and documentation, where a typo becomes a public API or a search miss."
subtechniques:
  - id: "V1003.001"
    name: "Identifier typo detection"
    slug: "identifier-typo-detection"
    description: "Split camelCase and snake_case identifiers and flag known misspellings."
  - id: "V1003.002"
    name: "Prose spell check"
    slug: "prose-spell-check"
    description: "Dictionary check over docs and comments with a project word list."
---
