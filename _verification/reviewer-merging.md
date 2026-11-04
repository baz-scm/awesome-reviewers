---
title: "Reviewer merging"
code: "V1041.003"
slug: "reviewer-merging"
technique: "Reviewer routing"
technique_id: "V1041"
technique_slug: "reviewer-routing"
tactic: "Code review"
tactic_id: "VA06"
description: "Combine overlapping reviewers so one concern is not reviewed twice."
repos: 0
craft:
  - "List reviewers that cover the same paths or topics."
  - "Merge overlapping reviewers into one with the combined instructions."
  - "Confirm each concern is covered by one reviewer after the merge."
reverse:
  - "A reviewer config where one entry replaces several overlapping entries."
  - "A changelog or commit note that records which reviewers were merged."
  - "Review assignments that name one reviewer per path."
packages: []
tools: []
examples: []
---
