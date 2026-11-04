---
title: "Exhaustive interleaving"
code: "V1029.001"
slug: "exhaustive-interleaving"
technique: "Concurrency model checking"
technique_id: "V1029"
technique_slug: "concurrency-model-checking"
tactic: "Formal"
tactic_id: "VA05"
description: "Enumerate all interleavings of a small test (loom)."
repos: 1
craft:
  - "Write a two- or three-thread test that uses loom primitives in place of std ones."
  - "Wrap the test body in loom::model so every interleaving is explored."
  - "Run the loom tests in a dedicated CI job with the cfg flag set."
reverse:
  - "A --cfg loom flag in RUSTFLAGS in CI configuration or a Makefile."
  - "Tests that call loom::model around a small concurrent data structure."
packages:
  - id: "loom"
    name: "loom"
    url: "https://github.com/tokio-rs/loom"
tools:
  - name: "loom"
    repos: 1
examples:
  - repo: "tokio-rs/tokio"
    tool: "loom"
    command: "loom via environment"
---
