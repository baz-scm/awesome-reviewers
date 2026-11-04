---
title: "Lockfile consistency"
id: "V1016"
slug: "lockfile-consistency"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Fails when the lockfile no longer matches the manifest, so CI installs exactly what was reviewed."
subtechniques:
  - id: "V1016.001"
    name: "Frozen install"
    description: "Install with the frozen or locked flag so a stale lockfile fails."
  - id: "V1016.002"
    name: "Lock check"
    description: "Regenerate the lock and fail on any diff."
packages:
  - id: "uv"
    name: "uv (uv lock --check)"
    url: "https://github.com/astral-sh/uv"
craft:
  - "Commit lockfiles for applications."
  - "Use frozen installs in CI (npm ci, uv sync --locked, cargo build --locked)."
  - "Add an explicit lock check step for clearer failures."
reverse:
  - "--frozen-lockfile, --locked or npm ci in CI."
  - "uv lock --check or a lockfile diff step."
---
