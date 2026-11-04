---
title: "Memory of facts and rules"
code: "V1037.004"
slug: "memory-of-facts-and-rules"
technique: "Reviewers learned from past reviews"
technique_id: "V1037"
technique_slug: "reviewers-learned-from-past-reviews"
tactic: "Code review"
tactic_id: "VA06"
description: "Extract facts from new discussions and match them to existing rules to update or add them."
repos: 0
craft:
  - "Extract a fact from each new discussion, such as a naming convention or a banned API."
  - "Search existing rules for a match before adding a new one."
  - "Update the matched rule when the new discussion changes it, otherwise add a new rule."
reverse:
  - "A memory store of rules or facts that references the source threads."
  - "An update history for a rule showing the discussions that changed it."
packages:
  - id: "mem0"
    name: "Mem0"
    url: "https://github.com/mem0ai/mem0"
tools: []
examples: []
---
