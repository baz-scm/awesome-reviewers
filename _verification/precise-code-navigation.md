---
title: "Precise code navigation"
code: "V1033.002"
slug: "precise-code-navigation"
technique: "Review context retrieval"
technique_id: "V1033"
technique_slug: "review-context-retrieval"
tactic: "Code review"
tactic_id: "VA06"
description: "Definitions and references from a compiler-grade index."
repos: 0
craft:
  - "Generate a SCIP index with the language's indexer on the default branch."
  - "Upload the index to the review tool's storage on each merge."
  - "Query definitions and references from the index for each changed symbol."
reverse:
  - "index.scip files or a SCIP indexing step in CI."
  - "A language indexer such as scip-typescript or scip-python in the build tooling."
packages:
  - id: "scip"
    name: "SCIP"
    url: "https://github.com/scip-code/scip"
tools: []
examples: []
---
