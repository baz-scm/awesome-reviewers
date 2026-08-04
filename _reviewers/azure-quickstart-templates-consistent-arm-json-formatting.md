---
title: Consistent ARM Json Formatting
description: 'For ARM templates, enforce deterministic JSON formatting and standardized
  property ordering to keep diffs small and templates readable.


  **Rules**

  1. **Keep property order consistent**: follow the Azure “sort order of properties”
  guidance (move keys to the expected order).'
repository: Azure/azure-quickstart-templates
label: Code Style
language: Json
comments_count: 4
repository_stars: 14846
---

For ARM templates, enforce deterministic JSON formatting and standardized property ordering to keep diffs small and templates readable.

**Rules**
1. **Keep property order consistent**: follow the Azure “sort order of properties” guidance (move keys to the expected order).
2. **Prefer multi-line formatting**: format arrays and nested objects across multiple lines (avoid single-line arrays/objects that can be rewritten differently by tooling).
3. **Trim safely for readability**: remove redundant fields only when it won’t break the schema/deployment (don’t delete required properties).
4. **Avoid formatting tool churn**: don’t rely on editors/formatters that collapse arrays/objects into single-line forms; apply the team’s formatting rules consistently.

**Example (safe trimming + multi-line style)**
```json
"subnets": [
  {
    "name": "subnet",
    "properties": {
      "addressPrefix": "192.168.0.0/24"
    }
  }
]
```
Apply the same formatting style across all templates, and reorder top-level/nested properties to match the prescribed ARM sort order before merging.