---
title: "Concurrency model checking"
id: "V1029"
slug: "concurrency-model-checking"
tactic: "Formal"
tactic_id: "VA05"
description: "Explores thread interleavings systematically to find races and orderings that fail only rarely."
subtechniques:
  - id: "V1029.001"
    name: "Exhaustive interleaving"
    description: "Enumerate all interleavings of a small test (loom)."
  - id: "V1029.002"
    name: "Randomized scheduling"
    description: "Sample schedules with a controlled scheduler (shuttle)."
packages:
  - id: "loom"
    name: "loom"
    url: "https://github.com/tokio-rs/loom"
  - id: "shuttle"
    name: "Shuttle"
    url: "https://github.com/awslabs/shuttle"
  - id: "sanitizers"
    name: "Sanitizers (ASan, TSan, UBSan)"
    url: "https://github.com/google/sanitizers"
craft:
  - "Isolate the concurrent primitive behind an interface the checker can swap."
  - "Write small tests with two or three threads."
  - "Run them in a dedicated CI job with the checker's cfg flag."
reverse:
  - "--cfg loom in RUSTFLAGS or loom::model in tests."
  - "ThreadSanitizer builds in CI."
---
