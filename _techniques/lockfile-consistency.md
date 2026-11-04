---
title: "Lockfile consistency"
code: "V1016"
slug: "lockfile-consistency"
tactic: "Supply chain"
tactic_id: "VA03"
description: "Fails when the lockfile no longer matches the manifest, so CI installs exactly what was reviewed."
subtechniques:
  - id: "V1016.001"
    name: "Frozen install"
    slug: "frozen-install"
    description: "Install with the frozen or locked flag so a stale lockfile fails."
  - id: "V1016.002"
    name: "Lock check"
    slug: "lock-check"
    description: "Regenerate the lock and fail on any diff."
---
