---
title: "Ephemeral environment"
code: "V1026.001"
slug: "ephemeral-environment"
technique: "Sandboxed execution"
technique_id: "V1026"
technique_slug: "sandboxed-execution"
tactic: "Testing"
tactic_id: "VA04"
description: "A fresh container or microVM per change with the repository's toolchain."
repos: 0
craft:
  - "Define the build and test environment in a Dagger pipeline or container image."
  - "Start a fresh container for each change and install the repository's dependencies inside it."
  - "Run the repository's own install, lint and test commands in that container."
reverse:
  - "A dagger.json, devcontainer.json or Dockerfile used by the CI job."
  - "CI logs that show the container image and the test commands run inside it."
packages:
  - id: "dagger"
    name: "Dagger"
    url: "https://github.com/dagger/dagger"
  - id: "e2b"
    name: "E2B"
    url: "https://github.com/e2b-dev/E2B"
  - id: "testcontainers"
    name: "Testcontainers (Python)"
    url: "https://github.com/testcontainers/testcontainers-python"
tools: []
examples: []
---
