---
title: "Large file guard"
code: "V1002.003"
slug: "large-file-guard"
technique: "File hygiene"
technique_id: "V1002"
technique_slug: "file-hygiene"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Refuse files above a size limit so binaries go to LFS or object storage."
repos: 33
craft:
  - "Enable check-added-large-files with a size limit that fits the repository."
  - "Track binary assets above the limit with Git LFS or move them to object storage."
  - "Allow-list a file only when it must live in the repository."
reverse:
  - "A check-added-large-files entry with a maxkb argument in .pre-commit-config.yaml."
  - "A .gitattributes file with filter=lfs patterns for binary asset types."
  - "No tracked blob in the repository is above the configured size limit."
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
