---
title: "Coverage-guided fuzzing"
code: "V1022.001"
slug: "coverage-guided-fuzzing"
technique: "Fuzzing"
technique_id: "V1022"
technique_slug: "fuzzing"
tactic: "Testing"
tactic_id: "VA04"
description: "libFuzzer or AFL style harnesses per entry point."
repos: 6
craft:
  - "Write one harness for each parser or decoder entry point."
  - "Build each harness with the coverage instrumentation the fuzzer requires."
  - "Run each harness for a fixed time budget locally and in CI."
reverse:
  - "A fuzz directory with one target file per parser entry point."
  - "A cargo fuzz target, atheris or jazzer harness that takes raw input bytes."
  - "Fuzzer command lines in a Makefile or workflow."
packages:
  - id: "cargo-fuzz"
    name: "cargo-fuzz"
    url: "https://github.com/rust-fuzz/cargo-fuzz"
  - id: "atheris"
    name: "Atheris"
    url: "https://github.com/google/atheris"
  - id: "jazzer"
    name: "Jazzer"
    url: "https://github.com/CodeIntelligenceTesting/jazzer"
  - id: "afl"
    name: "AFL++"
    url: "https://github.com/AFLplusplus/AFLplusplus"
tools:
  - name: "cargo-fuzz"
    repos: 6
examples:
  - repo: "astral-sh/ruff"
    tool: "cargo-fuzz"
    command: "cargo fuzz build -s none"
  - repo: "tokio-rs/tokio"
    tool: "cargo-fuzz"
    command: "cargo fuzz check --all-features"
---
