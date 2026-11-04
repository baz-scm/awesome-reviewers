---
title: "Sandboxed execution"
code: "V1026"
slug: "sandboxed-execution"
tactic: "Testing"
tactic_id: "VA04"
description: "Builds and runs the change in an isolated environment to confirm it installs, starts and passes its checks before anyone relies on it."
subtechniques:
  - id: "V1026.001"
    name: "Ephemeral environment"
    slug: "ephemeral-environment"
    description: "A fresh container or microVM per change with the repository's toolchain."
  - id: "V1026.002"
    name: "Reproduce-then-verify"
    slug: "reproduce-then-verify"
    description: "Reproduce a reported bug in the sandbox, apply the fix, and show the same command now passes."
---
