---
title: In-code Documentation Consistency
description: Ensure any developer-facing documentation embedded in the codebase (template
  metadata, links, and sample deployment instructions) is complete, unambiguous, portable,
  and consistent with the repository layout.
repository: Azure/azure-quickstart-templates
label: Documentation
language: Json
comments_count: 5
repository_stars: 14846
---

Ensure any developer-facing documentation embedded in the codebase (template metadata, links, and sample deployment instructions) is complete, unambiguous, portable, and consistent with the repository layout.

Apply this as a checklist when authoring/updating docs within code assets:
- **ARM/template parameter docs:** Every user-facing parameter must include `metadata.description` (no blanks or omissions).
- **Clarity in descriptions:** Define concepts precisely and avoid misleading phrasing. If a term is a composite (e.g., “unit = replica * partition”), either state that relationship or rewrite to describe the underlying building blocks.
- **Locale-neutral external links:** Don’t hardcode locale segments like `/en-us/` in doc URLs when the platform can select locale automatically.
- **README and deploy buttons alignment:** If a sample file is moved (e.g., `createUiDefinition.json`), update the README/deploy button targets so they reference the correct new path.

Example (ARM template parameter metadata):
```json
{
  "parameters": {
    "partitionCount": {
      "type": "int",
      "defaultValue": 1,
      "metadata": {
        "description": "Partitions are units of storage. Increasing partitions adds capacity and speed by spreading an index over multiple shards."
      }
    }
  }
}
```

Example (portable link pattern):
- Prefer `https://learn.microsoft.com/...` without hardcoded locale (e.g., avoid `/en-us/` when not required).