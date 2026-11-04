---
title: "Prompt optimization"
code: "V1068.001"
slug: "prompt-optimization"
technique: "Reviewer optimization"
technique_id: "V1068"
technique_slug: "reviewer-optimization"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Search prompt variants against a metric."
repos: 0
craft:
  - "Define the metric from the reviewer evaluation set first."
  - "Split the evaluation set into train and held-out parts."
  - "Keep a prompt variant only if it improves the held-out score."
reverse:
  - "An optimizer script that imports dspy or textgrad."
  - "Versioned prompt files in the repository with their held-out scores."
  - "An evaluation set file with train and held-out splits."
packages:
  - id: "dspy"
    name: "DSPy"
    url: "https://github.com/stanfordnlp/dspy"
  - id: "textgrad"
    name: "TextGrad"
    url: "https://github.com/zou-group/textgrad"
tools: []
examples: []
---
