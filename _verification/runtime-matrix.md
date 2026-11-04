---
title: "Runtime matrix"
code: "V1024.001"
slug: "runtime-matrix"
technique: "Version and platform matrix"
technique_id: "V1024"
technique_slug: "version-and-platform-matrix"
tactic: "Testing"
tactic_id: "VA04"
description: "Every supported language runtime version."
repos: 115
craft:
  - "List each supported runtime version in one place."
  - "Generate the CI matrix from that list so versions are not repeated."
  - "Run the oldest and newest versions on pull requests and the full matrix on the default branch."
reverse:
  - "strategy.matrix with a list of runtime versions in a workflow file."
  - "A tox.ini envlist or noxfile.py sessions that cover each runtime version."
  - "A supported-versions field in package metadata, such as python_requires or engines."
packages:
  - id: "tox"
    name: "tox"
    url: "https://github.com/tox-dev/tox"
  - id: "nox"
    name: "nox"
    url: "https://github.com/wntrblm/nox"
tools:
  - name: "ci-matrix"
    repos: 115
examples:
  - repo: "microsoft/vscode"
    tool: "ci-matrix"
    command: "analyze (include: 2)"
  - repo: "ollama/ollama"
    tool: "ci-matrix"
    command: "test (os: 3)"
  - repo: "30-seconds/30-seconds-of-code"
    tool: "ci-matrix"
    command: "js_tests (node-version: 1)"
  - repo: "langgenius/dify"
    tool: "ci-matrix"
    command: "api-unit (python-version: 1, shardIndex: 2, shardTotal: 1)"
  - repo: "nodejs/node"
    tool: "ci-matrix"
    command: "analyze (language: 3)"
---
