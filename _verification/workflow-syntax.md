---
title: "Workflow syntax"
code: "V1009.001"
slug: "workflow-syntax"
technique: "CI workflow linting"
technique_id: "V1009"
technique_slug: "ci-workflow-linting"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Validate workflow files and embedded shell before they run."
repos: 12
craft:
  - "Run actionlint on every file under .github/workflows."
  - "Install shellcheck beside actionlint so run: blocks are checked as shell."
  - "Make the actionlint check required before merge."
reverse:
  - "An actionlint step in a CI workflow or an actionlint entry in .pre-commit-config.yaml."
  - "Workflow files that pass actionlint with no suppression comments."
packages:
  - id: "actionlint"
    name: "actionlint"
    url: "https://github.com/rhysd/actionlint"
tools:
  - name: "actionlint"
    repos: 12
examples:
  - repo: "n8n-io/n8n"
    tool: "actionlint"
    command: "actionlint {staged_files}"
  - repo: "python/cpython"
    tool: "actionlint"
    command: "pre-commit hook actionlint"
  - repo: "vllm-project/vllm"
    tool: "actionlint"
    command: "pre-commit hook actionlint"
  - repo: "Homebrew/brew"
    tool: "actionlint"
    command: "actionlint"
  - repo: "astral-sh/ruff"
    tool: "actionlint"
    command: "pre-commit hook actionlint"
---
