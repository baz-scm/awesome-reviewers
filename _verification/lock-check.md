---
title: "Lock check"
code: "V1016.002"
slug: "lock-check"
technique: "Lockfile consistency"
technique_id: "V1016"
technique_slug: "lockfile-consistency"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Regenerate the lock and fail on any diff."
repos: 16
craft:
  - "Add a CI step that regenerates the lock file in check mode."
  - "Fail the step on any difference from the committed lock file."
  - "Print the diff in the job log so the fix is clear."
reverse:
  - "A workflow step running uv lock --check."
  - "A CI step that regenerates the lock and runs git diff --exit-code on it."
  - "A lock check step that runs before the install step."
packages:
  - id: "uv"
    name: "uv (uv lock --check)"
    url: "https://github.com/astral-sh/uv"
tools:
  - name: "uv-lock"
    repos: 16
examples:
  - repo: "TheAlgorithms/Python"
    tool: "uv-lock"
    command: "pre-commit hook uv-lock"
  - repo: "langgenius/dify"
    tool: "uv-lock"
    command: "uv lock --check"
  - repo: "pallets/flask"
    tool: "uv-lock"
    command: "pre-commit hook uv-lock"
  - repo: "apache/airflow"
    tool: "uv-lock"
    command: "uv lock --check"
  - repo: "astral-sh/ruff"
    tool: "uv-lock"
    command: "pre-commit hook uv-lock"
---
