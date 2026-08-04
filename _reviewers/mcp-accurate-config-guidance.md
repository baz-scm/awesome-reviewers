---
title: Accurate Config Guidance
description: 'When documenting configuration (env vars, parameters, tuning knobs,
  maintenance windows), ensure the guidance is actionable and operationally accurate—not
  just descriptive. In particular:'
repository: awslabs/mcp
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 9545
---

When documenting configuration (env vars, parameters, tuning knobs, maintenance windows), ensure the guidance is actionable and operationally accurate—not just descriptive. In particular:

- **State applicability/edition/scope**: If an option is Enterprise-only (or otherwise restricted), explicitly say so and direct Core/other editions to the correct alternative.
- **Make docs internally consistent**: Defaults, required fields, and parameter meanings must match across all config docs/tables (no “Default X” if the field is actually required with no default).
- **Include operational impact warnings**: If a configuration change can cause downtime or degraded service (e.g., patching during a maintenance window), document which components/instances are affected and recommend safe settings (e.g., low-traffic periods).
- **Be precise about auth/credentials**: Document the correct token/auth scheme and the full set of credential env vars required by the supported provider (e.g., include `AWS_SESSION_TOKEN` where relevant).

Example (config section pattern):
```md
### Embeddings Provider (AWS)
Required env vars:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
Optional (for temporary credentials):
- `AWS_SESSION_TOKEN`

### Tuning
`ingestQueryInstances` is **Enterprise-only**.
- Enterprise: set `ingestQueryInstances` in the parameter group.
- Core: use `--db-instance-type` vertical scaling instead.

### Maintenance Window
Changing the maintenance window may trigger patching and temporary downtime for affected instances. Use a low-traffic period.
```

Applying this standard prevents misconfiguration, reduces outages, and makes configuration docs trustworthy under real operational constraints.