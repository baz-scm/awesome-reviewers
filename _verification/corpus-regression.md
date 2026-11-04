---
title: "Corpus regression"
code: "V1022.003"
slug: "corpus-regression"
technique: "Fuzzing"
technique_id: "V1022"
technique_slug: "fuzzing"
tactic: "Testing"
tactic_id: "VA04"
description: "Replay the saved corpus and crash cases in normal CI."
repos: 6
craft:
  - "Commit the seed corpus and every crash case the fuzzer found."
  - "Replay the corpus in the normal test run without starting new fuzzing runs."
  - "Fail the build when a saved case crashes again."
reverse:
  - "A corpus or crashes directory next to the fuzz target."
  - "A CI step that replays the files in the corpus directory."
  - "Regression test names that refer to a fuzzing crash case."
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
