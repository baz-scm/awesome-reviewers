---
title: "Past discussion check"
id: "V1051"
slug: "past-discussion-check"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Compares a finding with earlier review discussions: a repeat of something already decided is suppressed, a regression of a fixed issue is raised."
subtechniques:
  - id: "V1051.001"
    name: "Repeat suppression"
    description: "Do not re-raise what a human already dismissed."
  - id: "V1051.002"
    name: "Regression detection"
    description: "Raise severity when a change reintroduces a previously fixed problem."
packages:
  - id: "mem0"
    name: "Mem0"
    url: "https://github.com/mem0ai/mem0"
  - id: "graphiti"
    name: "Graphiti"
    url: "https://github.com/getzep/graphiti"
  - id: "sentence-transformers"
    name: "Sentence Transformers"
    url: "https://github.com/huggingface/sentence-transformers"
craft:
  - "Store resolved and dismissed threads with their code location and outcome."
  - "Retrieve similar threads for each new finding."
  - "Suppress repeats; escalate regressions."
reverse:
  - "Resolved review threads that mention an earlier PR or issue."
---
