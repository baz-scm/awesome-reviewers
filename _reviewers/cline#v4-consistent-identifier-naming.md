---
title: Consistent Identifier Naming
description: All externally visible identifiers (JSON fields, hook names, config keys,
  event names) must use consistent, canonical names across products and versions.
  If naming must change, plan it as a deprecation—not a silent rename—and ensure documentation/config
  clearly states any build/rollout-specific naming.
repository: cline/cline#v4
label: Naming Conventions
language: Other
comments_count: 2
repository_stars: 70864
---

All externally visible identifiers (JSON fields, hook names, config keys, event names) must use consistent, canonical names across products and versions. If naming must change, plan it as a deprecation—not a silent rename—and ensure documentation/config clearly states any build/rollout-specific naming.

Apply this standard:
- Align first: When you find mismatched field names or identifier shapes across CLI/Desktop/VS Code (or “next” vs “legacy”), open/track a bug for each mismatch and converge on one canonical spelling.
- Deprecate explicitly: Keep legacy names working for a transition window, mark them as deprecated, and update all producers/consumers to the canonical name.
- Prevent silent drift: Add/adjust tests and fixtures so both old and new shapes are handled during the deprecation period, and remove legacy handling only after the window.
- Document rollout/build naming: If an identifier (e.g., a config key) differs by rollout/nightly/build identity, document the derivation rule (or the explicit values) so users set the right key and behavior isn’t “silently wrong.”

Example pattern (compatible rename):
```ts
// Canonical key
const CANONICAL_CONTEXT_KEY = "contextModification";
// Legacy key (deprecated)
const LEGACY_CONTEXT_KEY = "context";

function parseHookResponse(json: any) {
  const context = json[CANONICAL_CONTEXT_KEY] ?? json[LEGACY_CONTEXT_KEY];
  if (json[LEGACY_CONTEXT_KEY] !== undefined) {
    // log/metrics: legacy used
  }
  return { context };
}
```