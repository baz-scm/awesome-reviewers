---
title: "Missed bug analysis"
id: "V1066"
slug: "missed-bug-analysis"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "For each bug that escaped review, finds which technique should have caught it and why it did not, then clusters the causes."
subtechniques:
  - id: "V1066.001"
    name: "Root cause trace"
    description: "Replay the review trace for the PR that introduced the bug."
  - id: "V1066.002"
    name: "Cause clustering"
    description: "Cluster root causes to find the systematic gaps."
  - id: "V1066.003"
    name: "Eval set growth"
    description: "Add each missed bug to an evaluation set for the reviewers."
packages:
  - id: "langfuse"
    name: "Langfuse"
    url: "https://github.com/langfuse/langfuse"
  - id: "phoenix"
    name: "Arize Phoenix"
    url: "https://github.com/Arize-ai/phoenix"
  - id: "bertopic"
    name: "BERTopic"
    url: "https://github.com/MaartenGr/BERTopic"
craft:
  - "Link every bug fix to the PR that introduced the bug."
  - "Trace what each check and reviewer saw on that PR."
  - "Add the case to the eval set and re-run reviewers on it."
reverse:
  - "Postmortems that name the introducing PR, and tracing for review agents."
---
