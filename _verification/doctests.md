---
title: "Doctests"
code: "V1010.003"
slug: "doctests"
technique: "Documentation build"
technique_id: "V1010"
technique_slug: "documentation-build"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Run code examples in documentation as tests."
repos: 106
craft:
  - "Enable doctest collection, such as pytest --doctest-modules or cargo test for Rust doc comments."
  - "Write examples as runnable snippets with the expected output."
  - "Run the doctest step in the same CI job as the unit tests."
reverse:
  - "A pytest configuration with doctest_modules or doctest_glob set."
  - "Code examples in docstrings or doc comments that include expected output."
packages: []
tools:
  - name: "pytest"
    repos: 77
  - name: "cargo-test"
    repos: 44
examples:
  - repo: "facebook/react"
    tool: "cargo-test"
    command: "cargo test --workspace"
  - repo: "nousresearch/hermes-agent"
    tool: "pytest"
    command: "pytest ${args[@]}"
  - repo: "TheAlgorithms/Python"
    tool: "pytest"
    command: "pytest --iterations=8 --parallel-threads=auto --ignore-gil-enabled --ignore=computer_vision/flip_augmentation.py --ignore=computer_vision/harris_corner.py --ign"
  - repo: "microsoft/vscode"
    tool: "cargo-test"
    command: "cargo test ${args[@]}"
  - repo: "langchain-ai/langchain"
    tool: "pytest"
    command: "pytest -m compile tests/integration_tests"
---
