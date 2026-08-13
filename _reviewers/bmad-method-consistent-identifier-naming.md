---
title: Consistent Identifier Naming
description: 'Use deterministic, normalized identifiers everywhere.


  Apply two rules:

  1) Single source of truth: derive canonical identifiers from one stable place (e.g.,
  directory name), and don’t trust optional/conflicting metadata fields.'
repository: bmad-code-org/bmad-method
label: Naming Conventions
language: JavaScript
comments_count: 2
repository_stars: 51859
---

Use deterministic, normalized identifiers everywhere.

Apply two rules:
1) Single source of truth: derive canonical identifiers from one stable place (e.g., directory name), and don’t trust optional/conflicting metadata fields.
2) Normalize at the boundary: normalize identifier keys (especially casing) immediately when assigning/receiving config so downstream lookups are consistent.

Example patterns:

```js
// 1) Deterministic canonicalId from directory name only
const canonicalId = path.basename(dir); // ignore any manifest-provided canonicalId

// 2) Normalize IDE keys at assignment time
const ideKey = ide.toLowerCase();
config.ides = config.ides.map((ide) => ide.toLowerCase());
```

Also add guardrails:
- Emit a warning (or fail) if a conflicting identifier field is provided (e.g., a manifest `canonicalId` when the canonical value must come from the directory name).
- Update tests to assert the normalized/deterministic behavior.