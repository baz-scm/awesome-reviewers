---
title: Prefer Local Fallbacks
description: When a client-facing feature depends on “capability/behavior selection,”
  avoid unnecessary API calls if the client already has authoritative local state,
  and define clear precedence between computed defaults and explicit overrides.
repository: cline/cline#v24
label: API
language: TSX
comments_count: 2
repository_stars: 70891
---

When a client-facing feature depends on “capability/behavior selection,” avoid unnecessary API calls if the client already has authoritative local state, and define clear precedence between computed defaults and explicit overrides.

Apply this in two common ways:
1) Use local authority over redundant endpoints
- If the client can determine the relevant feature set (e.g., subscribed model availability / mode) from its local provider state, don’t fetch plan/entitlements from an endpoint just to mirror what the client already knows.
- If you must carry models from one source to another, allow the same failure modes to surface consistently instead of introducing extra API-driven branching.

2) Specify default-vs-override precedence (and test it)
- Compute defaults from environment/user preferences (e.g., `prefers-reduced-motion`).
- Ensure an explicit input (prop/parameter) overrides those computed defaults.
- Add tests for both: (a) environment-driven default and (b) explicit override.

Example pattern (behavior precedence):
```ts
function resolveScrollBehavior({ behavior, prefersReducedMotion }: {
  behavior?: ScrollBehavior;
  prefersReducedMotion: boolean;
}) {
  // Precedence: explicit wins
  if (behavior) return behavior;
  return prefersReducedMotion ? "auto" : "smooth";
}
```

Checklist
- Do we rely on an endpoint when local state is already authoritative?
- Is the precedence order (computed default vs explicit override) unambiguous?
- Are both paths covered by tests? (default behavior + override behavior)