---
title: "Model as judge"
code: "V1067.002"
slug: "model-as-judge"
technique: "Reviewer evaluation"
technique_id: "V1067"
technique_slug: "reviewer-evaluation"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "A judge model matches reviewer findings to the labelled bugs."
repos: 0
craft:
  - "Write a grading prompt that matches each reviewer finding to a labelled bug, or to none."
  - "Check the grader against a set of hand-labelled matches first."
  - "Report grader agreement with the hand labels alongside each score."
reverse:
  - "A grader prompt or rubric file in the eval directory."
  - "A config that sets a rubric-based grader assertion."
  - "A file of hand-labelled matches used to check the grader."
packages:
  - id: "inspect"
    name: "Inspect"
    url: "https://github.com/UKGovernmentBEIS/inspect_ai"
  - id: "promptfoo"
    name: "promptfoo"
    url: "https://github.com/promptfoo/promptfoo"
  - id: "deepeval"
    name: "DeepEval"
    url: "https://github.com/confident-ai/deepeval"
tools: []
examples: []
---
