---
title: "Randomized scheduling"
code: "V1029.002"
slug: "randomized-scheduling"
technique: "Concurrency model checking"
technique_id: "V1029"
technique_slug: "concurrency-model-checking"
tactic: "Formal"
tactic_id: "VA05"
description: "Sample schedules with a controlled scheduler (shuttle)."
repos: 0
craft:
  - "Write the concurrency test against shuttle's sync and thread types."
  - "Run it over a fixed number of random schedules with a recorded seed."
  - "Replay a failing seed locally to reproduce the interleaving."
reverse:
  - "shuttle listed in dev-dependencies with tests that call its check functions."
  - "CI logs that print the seed of a failing schedule."
packages:
  - id: "shuttle"
    name: "Shuttle"
    url: "https://github.com/awslabs/shuttle"
tools: []
examples: []
---
