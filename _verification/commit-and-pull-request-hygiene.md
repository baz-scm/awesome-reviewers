---
title: "Commit and pull request hygiene"
id: "V1004"
slug: "commit-and-pull-request-hygiene"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Rules on the change itself rather than the code: commit message format, PR description, size limits, required labels or linked tickets."
subtechniques:
  - id: "V1004.001"
    name: "Commit message lint"
    description: "Enforce a message convention so changelogs and release tooling can parse history."
  - id: "V1004.002"
    name: "Pull request rules"
    description: "Fail or warn when a PR is too large, lacks a description, or touches files without matching tests or docs."
packages:
  - id: "commitlint"
    name: "commitlint"
    url: "https://github.com/conventional-changelog/commitlint"
  - id: "danger"
    name: "Danger JS"
    url: "https://github.com/danger/danger-js"
craft:
  - "Write the rules you already enforce by hand in review as a Dangerfile or commitlint config."
  - "Start as warnings, then turn the rules people respect into failures."
  - "Keep size thresholds per directory, not global."
reverse:
  - "commitlint.config.js, a Dangerfile, or a PR title check in CI."
  - "Release tooling that parses conventional commits (release-please, semantic-release)."
---
