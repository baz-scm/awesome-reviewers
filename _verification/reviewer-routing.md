---
title: "Reviewer routing"
id: "V1041"
slug: "reviewer-routing"
tactic: "Code review"
tactic_id: "VA06"
description: "Chooses which specialist reviewers, human or automated, apply to a change based on its files, topics and history."
subtechniques:
  - id: "V1041.001"
    name: "Path ownership"
    description: "Route by file path ownership rules."
  - id: "V1041.002"
    name: "Semantic matching"
    description: "Match the change to reviewer descriptions by embedding similarity and reranking."
  - id: "V1041.003"
    name: "Reviewer merging"
    description: "Combine overlapping reviewers so one concern is not reviewed twice."
packages:
  - id: "sentence-transformers"
    name: "Sentence Transformers"
    url: "https://github.com/huggingface/sentence-transformers"
  - id: "rerankers"
    name: "rerankers"
    url: "https://github.com/AnswerDotAI/rerankers"
  - id: "setfit"
    name: "SetFit"
    url: "https://github.com/huggingface/setfit"
craft:
  - "Start with CODEOWNERS for humans."
  - "Describe each automated reviewer in one paragraph and match changes to it."
  - "Log which reviewer produced accepted findings and prune the rest."
reverse:
  - "CODEOWNERS, review assignment bots, or reviewer config files."
---
