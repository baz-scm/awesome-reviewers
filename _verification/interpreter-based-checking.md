---
title: "Interpreter-based checking"
code: "V1028.001"
slug: "interpreter-based-checking"
technique: "Undefined-behaviour detection"
technique_id: "V1028"
technique_slug: "undefined-behaviour-detection"
tactic: "Formal"
tactic_id: "VA05"
description: "Run tests under an interpreter that tracks every pointer (Miri)."
repos: 4
craft:
  - "Install the miri component with rustup on the CI runner."
  - "Run cargo miri test on the crates and test subset that contain unsafe code."
  - "Run Miri as its own CI job and fail the job on any reported undefined behaviour."
reverse:
  - "A cargo miri test step in a workflow, with MIRIFLAGS set in the CI environment."
  - "Test modules gated with cfg(miri) to skip code Miri cannot run."
packages:
  - id: "miri"
    name: "Miri"
    url: "https://github.com/rust-lang/miri"
tools:
  - name: "miri"
    repos: 4
examples:
  - repo: "zed-industries/zed"
    tool: "miri"
    command: "cargo miri clean"
  - repo: "pola-rs/polars"
    tool: "miri"
    command: "cargo miri setup"
  - repo: "tokio-rs/tokio"
    tool: "miri"
    command: "cargo miri nextest run --features full --lib --no-fail-fast"
  - repo: "sst/opencode"
    tool: "miri"
    command: "cargo miri setup"
---
