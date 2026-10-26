---
title: Align Identifier Names
description: Use a single canonical naming scheme for shared identifiers (JSON fields,
  event names, configuration keys) across product surfaces/build variants, and handle
  changes with explicit deprecation + aliasing.
repository: cline/cline#v12
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 70872
---

Use a single canonical naming scheme for shared identifiers (JSON fields, event names, configuration keys) across product surfaces/build variants, and handle changes with explicit deprecation + aliasing.

Apply this when:
- The same “concept” is represented by different field/key names in different implementations.
- Docs mention or imply setting keys that can vary by rollout variant (e.g., next vs legacy vs nightly).

Action checklist
- Define canonical names for the schema/keys (one source of truth).
- Add compatibility mappings for legacy names (accept old names, emit/advertise canonical names).
- Deprecate legacy names instead of silently removing them.
- Update docs to match the actual runtime derivation of keys/fields for each variant.
- Add automated checks/tests to prevent future divergence.

Example: hook field alignment
- Canonicalize the “context modification” field name (e.g., `contextModification`) while still accepting a legacy alias (e.g., `context`) during transition:

```js
// Pseudocode for schema normalization
function normalizeHookResponse(input) {
  const out = { ...input };
  // Accept legacy alias
  if (out.contextModification == null && out.context != null) {
    out.contextModification = out.context;
    // Optionally: keep `context` for compatibility until deprecation completes
  }
  return out;
}
```

- Ensure both producers/consumers use the canonical field name in emitted JSON; legacy names should be treated as inputs only during the deprecation window.