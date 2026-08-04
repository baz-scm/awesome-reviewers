---
title: Externalize sensitive identifiers
description: Do not hardcode subscription/workspace/tenant/customer identifiers in
  scripts or source code—even if they’re not “secrets.” These are identifying information
  that can leak via logs, UI, demos, screenshots, or reviews. Pass them in via parameters
  or configuration (env vars, secure pipeline variables, secret stores) and avoid
  echoing them.
repository: Azure/Azure-Sentinel
label: Security
language: Other
comments_count: 1
repository_stars: 6042
---

Do not hardcode subscription/workspace/tenant/customer identifiers in scripts or source code—even if they’re not “secrets.” These are identifying information that can leak via logs, UI, demos, screenshots, or reviews. Pass them in via parameters or configuration (env vars, secure pipeline variables, secret stores) and avoid echoing them.

Example pattern (PowerShell):

```powershell
Param(
  [Parameter(Mandatory=$true)] [string]$fork,
  [Parameter(Mandatory=$true)] [string]$branch,
  [Parameter(Mandatory=$true)] [string]$repoBaseFolder,
  [Parameter(Mandatory=$true)] [string]$subscriptionId
)

# Use $subscriptionId for auth/scope selection.
# Avoid writing it to console/UI unless necessary.
```

Apply this rule to any identifiers that map to an organization, account, workspace, subscription, tenant, or environment.