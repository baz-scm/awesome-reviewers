---
title: "Identifier typo detection"
code: "V1003.001"
slug: "identifier-typo-detection"
technique: "Spelling"
technique_id: "V1003"
technique_slug: "spelling"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Split camelCase and snake_case identifiers and flag known misspellings."
repos: 0
craft:
  - "Run typos over the source tree, which splits camelCase and snake_case identifiers before matching."
  - "Put domain identifiers in an allow list in _typos.toml instead of disabling the check."
  - "Run typos in pre-commit and in CI on every pull request."
reverse:
  - "A [default.extend-identifiers] or [default.extend-words] table in _typos.toml."
  - "A typos hook in .pre-commit-config.yaml or a typos step in a CI workflow."
packages:
  - id: "typos"
    name: "typos"
    url: "https://github.com/crate-ci/typos"
tools: []
examples: []
---
