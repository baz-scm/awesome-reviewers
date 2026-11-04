---
title: "Check mode gate"
code: "V1001.003"
slug: "check-mode-gate"
technique: "Formatting"
technique_id: "V1001"
technique_slug: "formatting"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Run the formatter with --check or --diff in CI so unformatted code fails instead of being rewritten."
repos: 162
craft:
  - "Add a CI job that runs the formatter in check mode, such as --check or --diff."
  - "Make the job fail on any drift and print the diff in the log."
  - "Run the same command in the pre-commit hook so contributors see the failure first."
reverse:
  - "A CI step running ruff format --check, prettier --check, biome format --check or cargo fmt -- --check."
  - "A workflow job that exits non-zero on unformatted files."
  - "A pre-commit hook configured with the same formatter arguments as CI."
packages:
  - id: "ruff"
    name: "Ruff"
    url: "https://github.com/astral-sh/ruff"
  - id: "black"
    name: "Black"
    url: "https://github.com/psf/black"
  - id: "prettier"
    name: "Prettier"
    url: "https://github.com/prettier/prettier"
  - id: "biome"
    name: "Biome"
    url: "https://github.com/biomejs/biome"
  - id: "rustfmt"
    name: "rustfmt"
    url: "https://github.com/rust-lang/rustfmt"
tools:
  - name: "ruff-format"
    repos: 43
  - name: "black"
    repos: 14
  - name: "prettier"
    repos: 98
  - name: "biome"
    repos: 24
  - name: "rustfmt"
    repos: 46
  - name: "gofmt"
    repos: 7
examples:
  - repo: "freeCodeCamp/freeCodeCamp"
    tool: "prettier"
    command: "prettier --write client/i18n/locales/**/*.json"
  - repo: "kamranahmedse/developer-roadmap"
    tool: "prettier"
    command: "prettier --write ."
  - repo: "nousresearch/hermes-agent"
    tool: "prettier"
    command: "prettier --write src/**/*.{ts,tsx} packages/**/*.{ts,tsx}"
  - repo: "TheAlgorithms/Python"
    tool: "ruff-format"
    command: "pre-commit hook ruff-format"
  - repo: "microsoft/vscode"
    tool: "rustfmt"
    command: "cargo fmt --check"
---
