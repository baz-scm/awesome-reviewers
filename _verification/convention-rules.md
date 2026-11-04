---
title: "Convention rules"
code: "V1005.002"
slug: "convention-rules"
technique: "Linting"
technique_id: "V1005"
technique_slug: "linting"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Project conventions encoded as lint rules instead of review comments."
repos: 175
craft:
  - "List each project convention that reviewers repeat, such as import order or naming."
  - "Enable the built-in rule for each convention where one exists, and write a custom rule where none does."
  - "Pin the linter version so rule changes do not surprise contributors."
reverse:
  - "Rule selections for naming or import order, such as ruff's N or I rule sets."
  - "A .golangci.yml linters list that enables revive or stylecheck."
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
