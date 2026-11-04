---
title: "Repository map"
code: "V1033.001"
slug: "repository-map"
technique: "Review context retrieval"
technique_id: "V1033"
technique_slug: "review-context-retrieval"
tactic: "Code review"
tactic_id: "VA06"
description: "A ranked map of symbols and files built from syntax trees."
repos: 0
craft:
  - "Parse each source file with tree-sitter to extract definitions and references."
  - "Rank symbols and files by how often they are referenced across the repository."
  - "Cache the map and rebuild it when files change on the default branch."
reverse:
  - "tree-sitter grammar packages in the review tooling's dependencies."
  - "A repo-map cache or generated symbol map file in the tooling."
packages:
  - id: "tree-sitter"
    name: "tree-sitter"
    url: "https://github.com/tree-sitter/tree-sitter"
  - id: "aider"
    name: "Aider"
    url: "https://github.com/Aider-AI/aider"
tools: []
examples: []
---
