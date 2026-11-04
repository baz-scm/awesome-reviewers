---
title: "Code formatter"
code: "V1001.001"
slug: "code-formatter"
technique: "Formatting"
technique_id: "V1001"
technique_slug: "formatting"
tactic: "Hygiene"
tactic_id: "VA01"
description: "One opinionated formatter per language, run on save and in CI."
repos: 162
craft:
  - "Choose one formatter for each language in the repository and pin its version."
  - "Commit its config file at the repository root, such as pyproject.toml or .prettierrc."
  - "Enable format on save in the shared editor settings and add a pre-commit hook that rewrites files."
reverse:
  - "Formatter config in pyproject.toml, .prettierrc, rustfmt.toml or biome.json."
  - "A pre-commit config that lists a formatter hook."
  - "Formatter versions pinned in dev dependencies or package.json."
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
