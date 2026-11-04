---
title: "Topic grouping"
code: "V1032.002"
slug: "topic-grouping"
technique: "Change intent extraction"
technique_id: "V1032"
technique_slug: "change-intent-extraction"
tactic: "Code review"
tactic_id: "VA06"
description: "Group changed files by topic and rate each topic's importance."
repos: 0
craft:
  - "Group the changed files by the feature or concern they touch, such as tests, API or migrations."
  - "Score each group by the risk of its changes and the number of callers affected."
  - "Show the groups as the suggested review order in the pull request description."
reverse:
  - "A .github/labeler.yml file that maps paths to topic labels."
  - "Pull request descriptions with headings that group changes by topic."
packages: []
tools: []
examples: []
---
