---
title: "Concurrency model checking"
code: "V1029"
slug: "concurrency-model-checking"
tactic: "Formal"
tactic_id: "VA05"
description: "Explores thread interleavings systematically to find races and orderings that fail only rarely."
subtechniques:
  - id: "V1029.001"
    name: "Exhaustive interleaving"
    slug: "exhaustive-interleaving"
    description: "Enumerate all interleavings of a small test (loom)."
  - id: "V1029.002"
    name: "Randomized scheduling"
    slug: "randomized-scheduling"
    description: "Sample schedules with a controlled scheduler (shuttle)."
---
