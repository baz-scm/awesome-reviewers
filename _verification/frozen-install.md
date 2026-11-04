---
title: "Frozen install"
code: "V1016.001"
slug: "frozen-install"
technique: "Lockfile consistency"
technique_id: "V1016"
technique_slug: "lockfile-consistency"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Install with the frozen or locked flag so a stale lockfile fails."
repos: 0
craft:
  - "Commit the lockfile for every application in the repository."
  - "Install with the frozen flag in CI, such as npm ci, uv sync --locked or cargo build --locked."
  - "Make the job fail when the lockfile is missing or out of date."
reverse:
  - "CI steps that run npm ci, pnpm install --frozen-lockfile or uv sync --locked."
  - "A committed package-lock.json, uv.lock or Cargo.lock at the repository root."
  - "Install commands in workflow files that never run a plain install."
packages:
  - id: "uv"
    name: "uv (uv lock --check)"
    url: "https://github.com/astral-sh/uv"
tools: []
examples: []
---
