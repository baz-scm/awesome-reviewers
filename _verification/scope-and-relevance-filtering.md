---
title: "Scope and relevance filtering"
id: "V1047"
slug: "scope-and-relevance-filtering"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Keeps only findings that belong to this change: on changed lines, within the PR's intent, and fixable without reworking unchanged code."
subtechniques:
  - id: "V1047.001"
    name: "Diff scoping"
    description: "Report only on changed lines or their immediate context."
  - id: "V1047.002"
    name: "Intent scoping"
    description: "Move findings outside the PR's intent to follow-up work."
  - id: "V1047.003"
    name: "Remediation scope"
    description: "Check whether the fix stays inside the diff or reaches unchanged code."
packages:
  - id: "reviewdog"
    name: "reviewdog"
    url: "https://github.com/reviewdog/reviewdog"
  - id: "danger"
    name: "Danger JS"
    url: "https://github.com/danger/danger-js"
craft:
  - "Filter by diff hunks first; it is cheap and removes most noise."
  - "Check each remaining finding against the stated intent."
  - "File out-of-scope findings as issues instead of review comments."
reverse:
  - "reviewdog -filter-mode settings, or bots that only comment on changed lines."
---
