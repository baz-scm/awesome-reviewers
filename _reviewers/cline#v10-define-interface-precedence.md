---
title: Define Interface Precedence
description: When designing/using client-facing APIs (REST calls, client interfaces,
  and component prop contracts), ensure the interface has an explicit, testable precedence
  order for defaults, fallbacks, and overrides.
repository: cline/cline#v10
label: API
language: TSX
comments_count: 2
repository_stars: 70869
---

When designing/using client-facing APIs (REST calls, client interfaces, and component prop contracts), ensure the interface has an explicit, testable precedence order for defaults, fallbacks, and overrides.

Concretely:
- Choose the correct source of truth for decisions: if local/provider state determines behavior, don’t gate it on an external “plan”/profile endpoint unnecessarily.
- Make default behavior honor platform/user preferences (accessibility, media queries, etc.).
- Allow explicit props/parameters to override defaults, but only after the default is computed deterministically.
- Add tests that cover both: (1) default behavior derived from the authoritative source/preference, and (2) explicit override behavior.

Example pattern (prop precedence over platform default):

```ts
function ScrollButton({ behavior, ...props }: { behavior?: "smooth" | "auto" }) {
  const prefersReducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  const resolvedBehavior = behavior ?? (prefersReducedMotion ? "auto" : "smooth");
  return <button {...props} style={{ scrollBehavior: resolvedBehavior }} />;
}
```

This keeps API/client behavior consistent, reduces unnecessary coupling to remote endpoints, and prevents regressions in user-facing accessibility/behavior contracts.