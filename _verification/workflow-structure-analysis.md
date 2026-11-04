---
title: "Workflow structure analysis"
code: "V1070.002"
slug: "workflow-structure-analysis"
technique: "CI failure analysis"
technique_id: "V1070"
technique_slug: "ci-failure-analysis"
tactic: "Feedback and evaluation"
tactic_id: "VA10"
description: "Map jobs and steps to the checks they run (the scanner behind this site does this)."
repos: 12
craft:
  - "Run actionlint on the workflow directory in CI."
  - "Parse each workflow into its jobs and steps and list the checks each one runs."
  - "Fail the job when a workflow has an error."
reverse:
  - "An actionlint step in a workflow or pre-commit config."
  - "Workflow files under .github/workflows that name jobs and steps."
  - "A generated list or diagram of jobs and the checks they run."
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
