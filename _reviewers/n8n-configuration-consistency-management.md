---
title: Configuration consistency management
description: When modifying configuration files, ensure all references to the changed
  values are updated consistently across the entire project. Configuration changes
  rarely exist in isolation - they often have ripple effects throughout the codebase.
repository: n8n-io/n8n
label: Configurations
language: Json
comments_count: 4
repository_stars: 122978
---

When modifying configuration files, ensure all references to the changed values are updated consistently across the entire project. Configuration changes rarely exist in isolation - they often have ripple effects throughout the codebase.

Key guidelines:
- When renaming package identifiers, check for references in scripts, tooling, and CI configurations
- When changing workspace paths or references, verify that all build and execution contexts still function correctly
- When modifying TypeScript path configurations, ensure all dependent builds and imports are updated

Example:
```diff
# If changing a package name in package.json:
-  "name": "n8n-monorepo",
+  "name": "n8n-official",

# Ensure all references are updated in dependent scripts:
- pnpm --filter n8n-monorepo
+ pnpm --filter n8n-official
```

Or when modifying workspace paths:
```diff
# In devcontainer.json:
-  "workspaceFolder": "/workspaces",
+  "workspaceFolder": "/workspaces/n8n",

# Ensure postCreateCommand and other scripts 
# are adjusted to work with the new path context
```

Similarly, when changing TypeScript references or path aliases, audit all dependent configurations to prevent build failures and ensure tooling compatibility.