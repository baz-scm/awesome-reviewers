---
title: "Labelled benchmark"
code: "V1067.001"
slug: "labelled-benchmark"
technique: "Reviewer evaluation"
technique_id: "V1067"
technique_slug: "reviewer-evaluation"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "PRs with known bugs and known clean changes."
repos: 0
craft:
  - "Collect changes that shipped with a known bug and changes that needed no comments."
  - "Label each case with the expected findings, or with none for the clean cases."
  - "Report recall on the bugs and precision on the findings for each run."
reverse:
  - "A benchmarks or eval directory with labelled case files."
  - "A CI job that runs the benchmark on each change to the reviewer."
  - "A results file that lists recall and precision per run."
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
