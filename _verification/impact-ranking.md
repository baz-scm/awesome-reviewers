---
title: "Impact ranking"
code: "V1065.002"
slug: "impact-ranking"
technique: "Alert deduplication and triage"
technique_id: "V1065"
technique_slug: "alert-deduplication-and-triage"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Rank by users affected, frequency and recency."
repos: 0
craft:
  - "Count the distinct users affected by each alert group, not only its events."
  - "Weight each group by how often it recurs over the last day or week."
  - "Sort the queue by the combined score before routing to a person or an automated fixer."
reverse:
  - "A query or dashboard panel that counts affected users per error group."
  - "A sort or score field on the triage queue that combines users affected and recency."
packages: []
tools: []
examples: []
---
