---
title: "Reviewer evaluation"
id: "V1067"
slug: "reviewer-evaluation"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Benchmarks reviewers on labelled changes: did they find the known bugs, and how many findings were wrong."
subtechniques:
  - id: "V1067.001"
    name: "Labelled benchmark"
    description: "PRs with known bugs and known clean changes."
  - id: "V1067.002"
    name: "Model as judge"
    description: "A judge model matches reviewer findings to the labelled bugs."
  - id: "V1067.003"
    name: "Side-by-side comparison"
    description: "Run two reviewer versions on the same set and compare."
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
craft:
  - "Build the set from real escaped bugs and from changes that needed no comments."
  - "Score recall on bugs and precision on findings."
  - "Gate reviewer changes on the benchmark."
reverse:
  - "eval/ or benchmarks/ directories with labelled cases."
---
