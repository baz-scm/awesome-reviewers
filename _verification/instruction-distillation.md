---
title: "Instruction distillation"
code: "V1037.003"
slug: "instruction-distillation"
technique: "Reviewers learned from past reviews"
technique_id: "V1037"
technique_slug: "reviewers-learned-from-past-reviews"
tactic: "Code review"
tactic_id: "VA06"
description: "Write one instruction per theme with examples from the threads."
repos: 0
craft:
  - "Write one instruction per cluster, stated as what to check and why."
  - "Attach two or three example threads from the cluster to each instruction."
  - "Test each instruction on pull requests that were not used to write it."
reverse:
  - "Instruction files with front matter and a body, one per review theme."
  - "Provenance files that link each instruction to its source discussions."
packages:
  - id: "awesome-reviewers"
    name: "Awesome Reviewers"
    url: "https://github.com/baz-scm/awesome-reviewers"
tools: []
examples: []
---
