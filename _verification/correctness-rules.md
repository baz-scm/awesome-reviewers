---
title: "Correctness rules"
code: "V1005.001"
slug: "correctness-rules"
technique: "Linting"
technique_id: "V1005"
technique_slug: "linting"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Rules for likely bugs: unused results, shadowing, unreachable code, wrong comparisons."
repos: 175
craft:
  - "Enable the bug-finding rule groups in the linter config, such as ruff's F and B sets or ESLint's recommended set."
  - "Fix or baseline existing findings before the lint job starts failing builds."
  - "Run the linter in CI on every pull request so new findings block merge."
reverse:
  - "A select or extend-select list under [tool.ruff.lint] that includes F and B rule codes."
  - "Clippy correctness lints set to deny in lib.rs or Cargo.toml [lints] tables."
  - "Inline noqa or eslint-disable comments that name a specific correctness rule."
packages:
  - id: "ruff"
    name: "Ruff"
    url: "https://github.com/astral-sh/ruff"
  - id: "eslint"
    name: "ESLint"
    url: "https://github.com/eslint/eslint"
  - id: "golangci-lint"
    name: "golangci-lint"
    url: "https://github.com/golangci/golangci-lint"
  - id: "clippy"
    name: "Clippy"
    url: "https://github.com/rust-lang/rust-clippy"
  - id: "error-prone"
    name: "Error Prone"
    url: "https://github.com/google/error-prone"
tools:
  - name: "ruff-check"
    repos: 64
  - name: "eslint"
    repos: 107
  - name: "golangci-lint"
    repos: 26
  - name: "clippy"
    repos: 45
examples:
  - repo: "freeCodeCamp/freeCodeCamp"
    tool: "eslint"
    command: "eslint --max-warnings 0"
  - repo: "nousresearch/hermes-agent"
    tool: "ruff-check"
    command: "ruff check --output-format json --exit-zero > $R/head/ruff.json"
  - repo: "TheAlgorithms/Python"
    tool: "ruff-check"
    command: "ruff check --output-format=github ."
  - repo: "microsoft/vscode"
    tool: "clippy"
    command: "cargo clippy ${args[@]} -- -D warnings"
  - repo: "ollama/ollama"
    tool: "golangci-lint"
    command: "uses golangci/golangci-lint-action"
---
