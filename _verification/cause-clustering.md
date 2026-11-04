---
title: "Cause clustering"
code: "V1066.002"
slug: "cause-clustering"
technique: "Missed bug analysis"
technique_id: "V1066"
technique_slug: "missed-bug-analysis"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Cluster root causes to find the systematic gaps."
repos: 0
craft:
  - "Gather the root-cause notes for all escaped bugs from the period."
  - "Cluster the notes by cause, such as a missing test, an unclear rule or a skipped file."
  - "Rank the clusters by count to pick the gaps to fix first."
reverse:
  - "A root-cause category field on each bug record."
  - "A summary file that lists clusters of missed-bug causes with counts."
packages:
  - id: "bertopic"
    name: "BERTopic"
    url: "https://github.com/MaartenGr/BERTopic"
tools: []
examples: []
---
