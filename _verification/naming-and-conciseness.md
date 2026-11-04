---
title: "Naming and conciseness"
code: "V1036.002"
slug: "naming-and-conciseness"
technique: "Convention and guideline review"
technique_id: "V1036"
technique_slug: "convention-and-guideline-review"
tactic: "Code review"
tactic_id: "VA06"
description: "Flag unclear names, typos and needless code."
repos: 22
craft:
  - "Run typos over the diff so misspelled new names and comments are caught."
  - "Flag new names that do not say what they hold, such as data2 or tmp in a long-lived function."
  - "Flag new helpers that duplicate an existing function in the same module."
reverse:
  - "A typos or codespell hook in .pre-commit-config.yaml."
  - "A review checklist in CONTRIBUTING.md that lists naming and conciseness rules."
packages:
  - id: "typos"
    name: "typos"
    url: "https://github.com/crate-ci/typos"
tools:
  - name: "codespell"
    repos: 22
examples:
  - repo: "TheAlgorithms/Python"
    tool: "codespell"
    command: "pre-commit hook codespell"
  - repo: "langflow-ai/langflow"
    tool: "codespell"
    command: "codespell --toml pyproject.toml"
  - repo: "home-assistant/core"
    tool: "codespell"
    command: "pre-commit hook codespell"
  - repo: "pallets/flask"
    tool: "codespell"
    command: "pre-commit hook codespell"
  - repo: "browser-use/browser-use"
    tool: "codespell"
    command: "pre-commit hook codespell"
---
