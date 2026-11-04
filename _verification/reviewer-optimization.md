---
title: "Reviewer optimization"
id: "V1068"
slug: "reviewer-optimization"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Tunes reviewer prompts and instructions against the evaluation set instead of by hand."
subtechniques:
  - id: "V1068.001"
    name: "Prompt optimization"
    description: "Search prompt variants against a metric."
  - id: "V1068.002"
    name: "Instruction updates from feedback"
    description: "Update reviewer instructions from accepted and rejected findings."
packages:
  - id: "dspy"
    name: "DSPy"
    url: "https://github.com/stanfordnlp/dspy"
  - id: "textgrad"
    name: "TextGrad"
    url: "https://github.com/zou-group/textgrad"
craft:
  - "Define the metric first (from reviewer evaluation)."
  - "Optimize on a train split; report on a held-out split."
  - "Review every prompt change like code."
reverse:
  - "Optimizer scripts and versioned prompt files in the repository."
---
