---
title: "Duplicate code detection"
id: "V1011"
slug: "duplicate-code-detection"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Finds copied blocks so a fix in one copy is not missed in the others, and flags new code that re-implements an existing helper."
subtechniques:
  - id: "V1011.001"
    name: "Token clone detection"
    description: "Report token-identical or near-identical blocks above a size threshold."
  - id: "V1011.002"
    name: "Semantic reuse check"
    description: "Search the codebase for an existing function that does what the new code does, by embedding or by name."
packages:
  - id: "jscpd"
    name: "jscpd"
    url: "https://github.com/kucherenko/jscpd"
  - id: "pmd"
    name: "PMD (CPD)"
    url: "https://github.com/pmd/pmd"
  - id: "sentence-transformers"
    name: "Sentence Transformers"
    url: "https://github.com/huggingface/sentence-transformers"
craft:
  - "Run a clone detector with a minimum token count that ignores tests and generated code."
  - "Report only clones introduced by the change."
  - "For reuse, index function signatures and docstrings and query with each new function."
reverse:
  - ".jscpd.json or a cpd task in the build."
  - "Review comments asking to reuse an existing helper point at where this is missing."
---
