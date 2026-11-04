---
title: "Discussion-aware reflection"
code: "V1050.002"
slug: "discussion-aware-reflection"
technique: "Reflection pass"
technique_id: "V1050"
technique_slug: "reflection-pass"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Include existing review threads so the reviewer does not repeat or contradict them."
repos: 0
craft:
  - "Fetch the existing review threads on the pull request before the pass starts."
  - "Pass each thread's text and resolved state into the pass."
  - "Drop a finding when an open thread already raises the same point, and flag any contradiction for a human."
reverse:
  - "A workflow step that reads review comments through the GitHub API before the review job runs."
  - "Finding records that cite the ID of an existing open thread."
packages: []
tools: []
examples: []
---
