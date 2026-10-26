---
title: Consistent Identifier Names
description: Use a single canonical naming scheme for any shared contract (JSON fields,
  event names, config keys) across all product surfaces, and treat divergences as
  bugs.
repository: cline/cline#v16
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 70882
---

Use a single canonical naming scheme for any shared contract (JSON fields, event names, config keys) across all product surfaces, and treat divergences as bugs.

Apply these rules:
1) Define canonical names per contract
- Pick one spelling/casing for each field/identifier (e.g., the JSON output fields your hook/event schema accepts).

2) No silent drift across products
- If you find a mismatch between products (CLI vs Desktop vs VS Code) in field names or config keys, file a bug for every mismatch.

3) Deprecate, don’t fork
- When renaming/aligning, keep the old name as a backward-compatible alias and deprecate it (with a clear removal plan). Prefer the canonical name in docs and new implementations.

4) Make variant-specific naming explicit and deterministic
- If rollout/variant identity affects keys (e.g., config key prefixes), generate keys deterministically from the variant identity and avoid behavior that “silently” routes users into the wrong bundle.

Example (hook JSON field alignment):
```js
// Preferred (canonical)
const payload = {
  cancel: true,
  errorMessage: 'Reason',
  contextModification: 'Added context'
};

// Backward-compatible alias (deprecated)
// accept old name but normalize internally
function normalizeHookResponse(input) {
  return {
    ...input,
    contextModification: input.context ?? input.contextModification
  };
}
```

Outcome: developers can rely on stable identifiers, docs match behavior, and legacy clients don’t break while you converge on one naming standard.