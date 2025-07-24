---
title: Use clear, descriptive names
description: Choose names that accurately describe their purpose and avoid unnecessary
  verbosity. Field names should semantically match what they contain or validate,
  and component names should be concise without redundant prefixes that don't add
  clarity.
repository: argoproj/argo-cd
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 20149
---

Choose names that accurately describe their purpose and avoid unnecessary verbosity. Field names should semantically match what they contain or validate, and component names should be concise without redundant prefixes that don't add clarity.

For example, when a field contains a validation pattern, use "format" instead of "type":
```lua
-- Instead of:
["type"] = "^[0-9]*$",

-- Use:
["format"] = "^[0-9]*$",
```

Similarly, avoid redundant prefixes in component names:
```yaml
# Instead of:
workload='argocd-repo-server'

# Use:
workload='repo-server'
```

This makes code more intuitive to read and components easier to find and reference.