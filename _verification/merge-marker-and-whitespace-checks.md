---
title: "Merge marker and whitespace checks"
code: "V1002.002"
slug: "merge-marker-and-whitespace-checks"
technique: "File hygiene"
technique_id: "V1002"
technique_slug: "file-hygiene"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Reject conflict markers, trailing whitespace and missing final newlines."
repos: 33
craft:
  - "Enable check-merge-conflict, trailing-whitespace and end-of-file-fixer from pre-commit-hooks."
  - "Run the hooks on staged files locally and on all files in CI."
  - "Fix existing hits in one commit before making the hooks required."
reverse:
  - "check-merge-conflict, trailing-whitespace or end-of-file-fixer ids in .pre-commit-config.yaml."
  - "A CI job that runs pre-commit run --all-files."
  - "No tracked text file contains lines starting with <<<<<<< or >>>>>>>."
packages:
  - id: "pre-commit-hooks"
    name: "pre-commit-hooks"
    url: "https://github.com/pre-commit/pre-commit-hooks"
tools:
  - name: "pre-commit-hooks"
    repos: 33
examples:
  - repo: "TheAlgorithms/Python"
    tool: "pre-commit-hooks"
    command: "pre-commit hook check-executables-have-shebangs"
  - repo: "langchain-ai/langchain"
    tool: "pre-commit-hooks"
    command: "pre-commit hook check-yaml"
  - repo: "langflow-ai/langflow"
    tool: "pre-commit-hooks"
    command: "pre-commit hook check-case-conflict"
  - repo: "fastapi/fastapi"
    tool: "pre-commit-hooks"
    command: "pre-commit hook check-added-large-files"
  - repo: "ggml-org/llama.cpp"
    tool: "pre-commit-hooks"
    command: "pre-commit hook trailing-whitespace"
---
