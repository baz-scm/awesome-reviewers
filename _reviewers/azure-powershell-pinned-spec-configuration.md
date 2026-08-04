---
title: Pinned Spec Configuration
description: 'When configuration files drive code generation (e.g., AutoRest README
  YAML), pin the exact spec snapshot and use the correct configuration semantics.

  '
repository: Azure/azure-powershell
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 4762
---

When configuration files drive code generation (e.g., AutoRest README YAML), pin the exact spec snapshot and use the correct configuration semantics.

**Standard**
1. **Pin spec inputs**: use a **git commit SHA** or an explicit **spec tag**; avoid branch-ambiguous references.
2. **Respect field meaning**: `module-version` is **generation metadata** (do not treat it as the shipped package version). Use `tag` (or equivalent) to select the underlying spec set.
3. **Follow `input-file` URL/path conventions**: the `input-file` entries must use the expected base path/template so generation pulls the intended files.

**Example (canonical pattern)**
```yaml
require:
  - $(this-folder)/../../readme.azure.noprofile.md

# Use a spec tag to select the spec content snapshot
# (module-version is generation metadata, not the shipped module version)
tag: package-2026-03-01-preview
module-version: 1.1.0

input-file:
  - https://github.com/Azure/azure-rest-api-specs/blob/$(commit)/specification/apimanagement/resource-manager/Microsoft.ApiManagement/ApiManagement/stable/2022-08-01/apimanagement.json
```

Apply this rule to any AutoRest/config-driven SDK generation changes to keep outputs reproducible and prevent accidental mismatches between generation metadata and released artifacts.