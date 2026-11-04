---
title: "CI workflow linting"
id: "V1009"
slug: "ci-workflow-linting"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Checks CI definitions themselves: syntax, script injection through untrusted inputs, over-broad token permissions, unpinned actions."
subtechniques:
  - id: "V1009.001"
    name: "Workflow syntax"
    description: "Validate workflow files and embedded shell before they run."
  - id: "V1009.002"
    name: "Workflow security audit"
    description: "Flag template injection, pull_request_target misuse, unpinned third-party actions and write-all permissions."
packages:
  - id: "actionlint"
    name: "actionlint"
    url: "https://github.com/rhysd/actionlint"
  - id: "zizmor"
    name: "zizmor"
    url: "https://github.com/zizmorcore/zizmor"
  - id: "shellcheck"
    name: "ShellCheck"
    url: "https://github.com/koalaman/shellcheck"
craft:
  - "Run actionlint on every change to .github/workflows."
  - "Add zizmor and fix its high findings first: injection and permissions."
  - "Pin third-party actions to commit SHAs."
reverse:
  - "actionlint or zizmor in CI or pre-commit."
  - "permissions: blocks at workflow level and SHA-pinned uses: lines."
---
