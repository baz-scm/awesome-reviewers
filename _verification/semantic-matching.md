---
title: "Semantic matching"
code: "V1041.002"
slug: "semantic-matching"
technique: "Reviewer routing"
technique_id: "V1041"
technique_slug: "reviewer-routing"
tactic: "Code review"
tactic_id: "VA06"
description: "Match the change to reviewer descriptions by embedding similarity and reranking."
repos: 0
craft:
  - "Write a one-paragraph description for each automated reviewer."
  - "Embed each description and a summary of each changed file."
  - "Rerank the top matches and assign reviewers above a set score."
reverse:
  - "A reviewer description file that the routing script reads."
  - "A routing script or bot config that scores changes against reviewer descriptions."
  - "Routing decisions logged on pull requests with their scores."
packages:
  - id: "sentence-transformers"
    name: "Sentence Transformers"
    url: "https://github.com/huggingface/sentence-transformers"
  - id: "rerankers"
    name: "rerankers"
    url: "https://github.com/AnswerDotAI/rerankers"
tools: []
examples: []
---
