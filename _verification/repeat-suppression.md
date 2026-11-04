---
title: "Repeat suppression"
code: "V1051.001"
slug: "repeat-suppression"
technique: "Past discussion check"
technique_id: "V1051"
technique_slug: "past-discussion-check"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Do not re-raise what a human already dismissed."
repos: 0
craft:
  - "Store each dismissed thread with its file path and the reason it was dismissed."
  - "Compare each new finding with stored threads using embedding similarity."
  - "Suppress the finding when a similar dismissed thread is above the similarity threshold."
reverse:
  - "A store of dismissed threads, such as a JSON file or memory database, in the review tooling."
  - "A similarity threshold setting in the review configuration."
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
tools: []
examples: []
---
