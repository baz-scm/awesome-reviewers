---
title: "Semantic dedup"
code: "V1045.001"
slug: "semantic-dedup"
technique: "Finding deduplication"
technique_id: "V1045"
technique_slug: "finding-deduplication"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Cluster findings by embedding similarity and location."
repos: 0
craft:
  - "Embed each finding's message and code excerpt with a fixed sentence encoder."
  - "Group findings that have close vectors and sit in the same file."
  - "Review the groups in a log before merging them automatically."
reverse:
  - "A dedup script that imports sentence_transformers or faiss."
  - "An index file or cache of finding vectors in a build artifact."
  - "A threshold constant that sets the similarity cut-off."
packages:
  - id: "sentence-transformers"
    name: "Sentence Transformers"
    url: "https://github.com/huggingface/sentence-transformers"
  - id: "faiss"
    name: "FAISS"
    url: "https://github.com/facebookresearch/faiss"
tools: []
examples: []
---
