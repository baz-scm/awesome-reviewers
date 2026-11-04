---
title: "Merge rules"
code: "V1057.001"
slug: "merge-rules"
technique: "Merge readiness"
technique_id: "V1057"
technique_slug: "merge-readiness"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Required checks, approvals and labels as code."
repos: 0
craft:
  - "Write required checks, approvals and labels in a repository config file."
  - "Set branch protection so the same requirements apply on the platform."
  - "Enable auto-merge only for pull requests that meet every rule."
reverse:
  - ".kodiak.toml or a merge queue config file at the repository root."
  - "Branch protection rules that list required status checks."
  - "Pull requests that merge automatically after the last required approval."
packages:
  - id: "kodiak"
    name: "Kodiak"
    url: "https://github.com/chdsbd/kodiak"
tools: []
examples: []
---
