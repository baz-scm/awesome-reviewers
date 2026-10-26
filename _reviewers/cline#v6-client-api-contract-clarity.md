---
title: Client API Contract Clarity
description: 'When designing or consuming client/component “APIs”, ensure the contract
  is correct and predictable: choose the authoritative data source, make precedence
  rules explicit, and guarantee deterministic (localized) outputs.'
repository: cline/cline#v6
label: API
language: TSX
comments_count: 3
repository_stars: 70864
---

When designing or consuming client/component “APIs”, ensure the contract is correct and predictable: choose the authoritative data source, make precedence rules explicit, and guarantee deterministic (localized) outputs.

Apply:
1) Prefer local authority over unnecessary backend calls—don’t fetch user state from endpoints if the client can derive the same decision reliably.
2) Define behavioral precedence in the component API (e.g., defaults derived from environment/user preference, with explicit props overriding).
3) Treat user-visible summaries as part of the API contract: use locale-safe formatting and return explicit fallbacks when there’s no data.

Example (precedence):
```ts
function MessageScrollerButton({ direction = "end", behavior, children }: { behavior?: "smooth" | "auto" }) {
  const prefersReduced = window.matchMedia?.("(prefers-reduced-motion: reduce)")?.matches
  const resolvedBehavior = behavior ?? (prefersReduced ? "auto" : "smooth")
  return <Primitive.Button data-direction={direction} data-behavior={resolvedBehavior}>{children}</Primitive.Button>
}
```