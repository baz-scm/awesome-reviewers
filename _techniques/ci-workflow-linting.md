---
title: "CI workflow linting"
code: "V1009"
slug: "ci-workflow-linting"
tactic: "Static analysis"
tactic_id: "VA02"
description: "Checks CI definitions themselves: syntax, script injection through untrusted inputs, over-broad token permissions, unpinned actions."
subtechniques:
  - id: "V1009.001"
    name: "Workflow syntax"
    slug: "workflow-syntax"
    description: "Validate workflow files and embedded shell before they run."
  - id: "V1009.002"
    name: "Workflow security audit"
    slug: "workflow-security-audit"
    description: "Flag template injection, pull_request_target misuse, unpinned third-party actions and write-all permissions."
---
