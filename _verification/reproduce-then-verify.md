---
title: "Reproduce-then-verify"
code: "V1026.002"
slug: "reproduce-then-verify"
technique: "Sandboxed execution"
technique_id: "V1026"
technique_slug: "sandboxed-execution"
tactic: "Testing"
tactic_id: "VA04"
description: "Reproduce a reported bug in the sandbox, apply the fix, and show the same command now passes."
repos: 0
craft:
  - "Run the reported reproduction steps in an isolated sandbox before any fix is written."
  - "Apply the fix in the same sandbox and run the same command again."
  - "Attach both command outputs to the pull request."
reverse:
  - "Pull request comments that include reproduction output from a sandbox run."
  - "Regression tests named after the bug that fail before the fix and pass after it."
packages:
  - id: "e2b"
    name: "E2B"
    url: "https://github.com/e2b-dev/E2B"
tools: []
examples: []
---
