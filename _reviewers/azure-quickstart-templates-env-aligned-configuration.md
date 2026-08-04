---
title: Env-Aligned Configuration
description: 'When a solution has environment-specific configuration (e.g., public
  vs US Gov) or requires cloud-context values, ensure:

  1) **Environment-specific UI/artifacts are derived from the declared support matrix**
  (e.g., `metadata.json` → `environments`). If an environment is not supported, do
  not render its corresponding badge/button/link.'
repository: Azure/azure-quickstart-templates
label: Configurations
language: Markdown
comments_count: 2
repository_stars: 14846
---

When a solution has environment-specific configuration (e.g., public vs US Gov) or requires cloud-context values, ensure:
1) **Environment-specific UI/artifacts are derived from the declared support matrix** (e.g., `metadata.json` → `environments`). If an environment is not supported, do not render its corresponding badge/button/link.
2) **Configuration values should come from a single source of truth**—prefer platform/intrinsic functions over manual user parameters when the value is already available from the deployment context.

Example (ARM/Template): derive `tenantId` instead of asking the user for it
```bicep
// Instead of a user-provided parameter tenantId
// parameter tenantId string
// Use the platform context:
var tenantId = subscription().tenantId
```

Example (README/badges/buttons): render only supported environments
- Ensure each badge/button (e.g., Public vs US Gov) is conditionally included based on `metadata.json`’s `environments` support.
- Practically: run/align with the project’s metadata validation logic (such as a `Validate-Metadata` script) so the UI and deployment targets cannot drift from the environment support declaration.