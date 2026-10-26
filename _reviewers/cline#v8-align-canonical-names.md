---
title: Align Canonical Names
description: 'Use a single canonical naming scheme for shared schemas/identifiers
  across all product surfaces (CLI/Desktop/VS Code, rollout variants, etc.). If names
  diverge, treat it as a compatibility bug: align to the canonical field/key names
  and deprecate the old names with a transition period.'
repository: cline/cline#v8
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 70867
---

Use a single canonical naming scheme for shared schemas/identifiers across all product surfaces (CLI/Desktop/VS Code, rollout variants, etc.). If names diverge, treat it as a compatibility bug: align to the canonical field/key names and deprecate the old names with a transition period.

Apply this standard when:
- JSON schemas, event names, or field names differ between implementations.
- Configuration/settings keys are derived from rollout identities and lead to different behavior.
- Documentation introduces new naming terms that would otherwise be misleading for specific builds.

Operational guidance
- Define canonical names (one set of field names/keys that everything should converge on).
- Fix mismatches by updating implementations to use canonical names.
- Deprecate old names: accept both during transition, but emit warnings and plan removal.
- Backward compatibility: provide mapping/aliases (e.g., accept legacy JSON field names) until deprecation completes.
- Documentation: when variant-specific mapping exists (nightly/rollout), state it clearly and tie it to the exact naming/key users must set.

Example pattern (schema aliasing during rename)
```js
function normalizeHookInput(input) {
  // Canonical field name
  const canonical = {
    cancel: input.cancel,
    errorMessage: input.errorMessage,
    contextModification: input.contextModification ?? input.context, // legacy alias
  };

  // Optional: warn when legacy names are used
  if (input.context !== undefined && input.contextModification === undefined) {
    console.warn('Deprecated: use contextModification instead of context');
  }

  return canonical;
}
```