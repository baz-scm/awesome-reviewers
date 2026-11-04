---
title: "Spelling"
id: "V1003"
slug: "spelling"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Finds misspellings in identifiers, comments and documentation, where a typo becomes a public API or a search miss."
subtechniques:
  - id: "V1003.001"
    name: "Identifier typo detection"
    description: "Split camelCase and snake_case identifiers and flag known misspellings."
  - id: "V1003.002"
    name: "Prose spell check"
    description: "Dictionary check over docs and comments with a project word list."
packages:
  - id: "typos"
    name: "typos"
    url: "https://github.com/crate-ci/typos"
  - id: "codespell"
    name: "codespell"
    url: "https://github.com/codespell-project/codespell"
  - id: "cspell"
    name: "CSpell"
    url: "https://github.com/streetsidesoftware/cspell"
craft:
  - "Start with a low false-positive tool (typos or codespell) on the whole tree."
  - "Add an allow-list file for domain words instead of disabling the check."
  - "Run it in pre-commit and in CI with autofix locally."
reverse:
  - "_typos.toml, .codespellrc or cspell.json in the repository."
  - "A codespell or typos hook in .pre-commit-config.yaml."
---
