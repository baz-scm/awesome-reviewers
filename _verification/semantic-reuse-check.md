---
title: "Semantic reuse check"
code: "V1011.002"
slug: "semantic-reuse-check"
technique: "Duplicate code detection"
technique_id: "V1011"
technique_slug: "duplicate-code-detection"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Search the codebase for an existing function that does what the new code does, by embedding or by name."
repos: 0
craft:
  - "Embed the signature and docstring of each existing function in the repository."
  - "Query that index with each new function and show the nearest matches in review."
  - "Ask the author to reuse or justify a new helper that closely matches an existing one."
reverse:
  - "An index build script or cached embedding file for function signatures."
  - "A CI or bot step that posts nearest-match suggestions on new functions."
  - "Review comments that point to an existing helper for a new function."
packages:
  - id: "sentence-transformers"
    name: "Sentence Transformers"
    url: "https://github.com/huggingface/sentence-transformers"
tools: []
examples: []
---
