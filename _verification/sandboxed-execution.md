---
title: "Sandboxed execution"
id: "V1026"
slug: "sandboxed-execution"
tactic: "Testing"
tactic_id: "VA04"
description: "Builds and runs the change in an isolated environment to confirm it installs, starts and passes its checks before anyone relies on it."
subtechniques:
  - id: "V1026.001"
    name: "Ephemeral environment"
    description: "A fresh container or microVM per change with the repository's toolchain."
  - id: "V1026.002"
    name: "Reproduce-then-verify"
    description: "Reproduce a reported bug in the sandbox, apply the fix, and show the same command now passes."
packages:
  - id: "e2b"
    name: "E2B"
    url: "https://github.com/e2b-dev/E2B"
  - id: "dagger"
    name: "Dagger"
    url: "https://github.com/dagger/dagger"
  - id: "testcontainers"
    name: "Testcontainers (Python)"
    url: "https://github.com/testcontainers/testcontainers-python"
craft:
  - "Describe the environment as code (a Dagger pipeline or container image)."
  - "Run the repository's own install, lint and test commands inside it."
  - "Keep the logs as evidence attached to the change."
reverse:
  - "dagger.json, devcontainer.json or a setup script used by CI."
  - "Bots that post reproduction logs on issues or PRs."
---
