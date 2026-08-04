---
title: Enforce Security Prereqs
description: 'Ensure infrastructure/code templates explicitly and correctly handle
  the two most common security failure points: (1) required authorization for identities
  to perform discovery/monitoring, and (2) strict validation of user-supplied parameters.'
repository: Azure/azure-quickstart-templates
label: Security
language: Markdown
comments_count: 2
repository_stars: 14846
---

Ensure infrastructure/code templates explicitly and correctly handle the two most common security failure points: (1) required authorization for identities to perform discovery/monitoring, and (2) strict validation of user-supplied parameters.

Apply this as a checklist:
- Authorization (RBAC):
  - Document and implement the exact role assignment(s) required for the managed identity/service to access target resources.
  - If discovery/monitoring depends on permissions, make it a “must-do” step early; otherwise the deployment may succeed but produce no discovered entities.
  - Prefer least-privilege scoping (e.g., subscription/resource group) where appropriate, rather than repeating assignments on every resource.
- Input validation (template parameters):
  - For any required string parameters (names/IDs), add min/max length constraints (and other validation) so invalid values fail fast at deployment time.

Example (Bicep/ARM-style validation + scoped RBAC intent):
```bicep
param healthModelName string(minLength: 3, maxLength: 50) // validate required inputs

// RBAC (conceptual): assign the managed identity the needed monitoring/discovery permissions
// at the smallest practical scope (resource group / subscription) instead of per-resource.
// (Implement using the template’s RBAC assignment constructs and the correct role definition.)
```
This prevents silent security/authorization failures (no effective access) and reduces misconfiguration risk by rejecting invalid inputs early.