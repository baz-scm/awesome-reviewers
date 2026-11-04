---
title: "Commit message lint"
code: "V1004.001"
slug: "commit-message-lint"
technique: "Commit and pull request hygiene"
technique_id: "V1004"
technique_slug: "commit-and-pull-request-hygiene"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Enforce a message convention so changelogs and release tooling can parse history."
repos: 0
craft:
  - "Add a commitlint config that sets the allowed types and scope rules."
  - "Install a commit-msg hook so non-conforming messages are rejected locally."
  - "Run the same check on every commit in pull requests in CI."
reverse:
  - "A commitlint.config.js or commitlint.config.ts at the repository root."
  - "A commit-msg hook in the husky or pre-commit setup that runs commitlint."
  - "Release tooling that reads commit types from history, such as release-please."
packages:
  - id: "commitlint"
    name: "commitlint"
    url: "https://github.com/conventional-changelog/commitlint"
tools: []
examples: []
---
