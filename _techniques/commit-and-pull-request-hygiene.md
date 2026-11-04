---
title: "Commit and pull request hygiene"
code: "V1004"
slug: "commit-and-pull-request-hygiene"
tactic: "Hygiene"
tactic_id: "VA01"
description: "Rules on the change itself rather than the code: commit message format, PR description, size limits, required labels or linked tickets."
subtechniques:
  - id: "V1004.001"
    name: "Commit message lint"
    slug: "commit-message-lint"
    description: "Enforce a message convention so changelogs and release tooling can parse history."
  - id: "V1004.002"
    name: "Pull request rules"
    slug: "pull-request-rules"
    description: "Fail or warn when a PR is too large, lacks a description, or touches files without matching tests or docs."
---
