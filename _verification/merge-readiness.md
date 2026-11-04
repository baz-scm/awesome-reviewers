---
title: "Merge readiness"
id: "V1057"
slug: "merge-readiness"
tactic: "Intent and spec conformance"
tactic_id: "VA08"
description: "Combines checks, reviews, open threads and findings into one verdict on whether a change can merge."
subtechniques:
  - id: "V1057.001"
    name: "Merge rules"
    description: "Required checks, approvals and labels as code."
  - id: "V1057.002"
    name: "Merge verdict summary"
    description: "A summary of what is still blocking, with links."
packages:
  - id: "kodiak"
    name: "Kodiak"
    url: "https://github.com/chdsbd/kodiak"
  - id: "danger"
    name: "Danger JS"
    url: "https://github.com/danger/danger-js"
craft:
  - "Encode required checks and approvals in branch protection."
  - "Add a bot that lists what is still blocking."
  - "Merge automatically only when the verdict is clean."
reverse:
  - "Branch protection rules, .kodiak.toml or merge queue config."
---
