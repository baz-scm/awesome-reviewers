---
title: "Run to confirm"
code: "V1042.003"
slug: "run-to-confirm"
technique: "Evidence-backed verification"
technique_id: "V1042"
technique_slug: "evidence-backed-verification"
tactic: "Finding validation"
tactic_id: "VA07"
description: "Write and run a test or script that demonstrates the failure."
repos: 0
craft:
  - "Write a test or script that reproduces the claimed failure."
  - "Run it in an isolated environment and keep the output."
  - "Confirm only findings whose script fails for the stated reason."
reverse:
  - "Pull request comments that include the output of a failing reproduction script."
  - "Scratch test files or sandbox run logs attached to review verdicts."
packages:
  - id: "e2b"
    name: "E2B"
    url: "https://github.com/e2b-dev/E2B"
tools: []
examples: []
---
