---
title: "Eval set growth"
code: "V1066.003"
slug: "eval-set-growth"
technique: "Missed bug analysis"
technique_id: "V1066"
technique_slug: "missed-bug-analysis"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Add each missed bug to an evaluation set for the reviewers."
repos: 0
craft:
  - "Add each missed bug as a test case with the diff and the expected finding."
  - "Keep the cases in the evaluation dataset that the reviewers run against."
  - "Re-run the reviewers on the set after every change to a rule."
reverse:
  - "An evaluation dataset file or configuration, such as promptfoo test cases or a Langfuse dataset."
  - "Test cases named after the bug or pull request they came from."
packages:
  - id: "langfuse"
    name: "Langfuse"
    url: "https://github.com/langfuse/langfuse"
  - id: "promptfoo"
    name: "promptfoo"
    url: "https://github.com/promptfoo/promptfoo"
tools: []
examples: []
---
