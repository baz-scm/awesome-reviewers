---
title: "Root cause trace"
code: "V1066.001"
slug: "root-cause-trace"
technique: "Missed bug analysis"
technique_id: "V1066"
technique_slug: "missed-bug-analysis"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Replay the review trace for the PR that introduced the bug."
repos: 0
craft:
  - "Link each escaped bug to the pull request that introduced it."
  - "Replay the review trace for that pull request and record what each check saw."
  - "Write down which check should have caught the bug and why it did not."
reverse:
  - "Postmortem notes that name the introducing pull request and the missed check."
  - "Tracing setup for review runs in the tooling, such as Langfuse or Phoenix SDK configuration."
packages:
  - id: "langfuse"
    name: "Langfuse"
    url: "https://github.com/langfuse/langfuse"
  - id: "phoenix"
    name: "Arize Phoenix"
    url: "https://github.com/Arize-ai/phoenix"
tools: []
examples: []
---
