---
title: "Prose spell check"
code: "V1003.002"
slug: "prose-spell-check"
technique: "Spelling"
technique_id: "V1003"
technique_slug: "spelling"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Dictionary check over docs and comments with a project word list."
repos: 22
craft:
  - "Run codespell over docs and comments in the repository."
  - "Keep domain words in a project word list such as cspell.json words or a .codespellrc ignore-words-list."
  - "Run the check in pre-commit and in CI on every pull request."
reverse:
  - "A .codespellrc or cspell.json file listing project words."
  - "A codespell or cspell hook in .pre-commit-config.yaml."
packages:
  - id: "cspell"
    name: "CSpell"
    url: "https://github.com/streetsidesoftware/cspell"
  - id: "codespell"
    name: "codespell"
    url: "https://github.com/codespell-project/codespell"
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
