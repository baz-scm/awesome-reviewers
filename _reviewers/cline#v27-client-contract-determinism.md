---
title: Client Contract Determinism
description: When implementing client-facing interfaces (including UI component behavior
  and client decisions about server capabilities), ensure behavior is driven by the
  most authoritative local/platform source, with explicit and tested precedence rules.
repository: cline/cline#v27
label: API
language: TSX
comments_count: 2
repository_stars: 70892
---

When implementing client-facing interfaces (including UI component behavior and client decisions about server capabilities), ensure behavior is driven by the most authoritative local/platform source, with explicit and tested precedence rules.

Apply this standard:
- Avoid redundant or stale server “capability” lookups when local state already represents the user’s effective entitlement (e.g., capability determined by a local provider/model selection rather than a separate plan endpoint).
- For default behavior, respect platform/user preferences (e.g., `prefers-reduced-motion`) instead of hardcoding UI behavior.
- Define precedence clearly: **system/user preference defaults** → overridden by **explicit props** or **explicit caller intent**.
- Add tests covering both the default path (preference-driven) and the override path (explicit prop winning).

Example pattern (precedence with system preference):
```ts
function resolveScrollBehavior(requested?: ScrollBehavior) {
  // default from user/system preference
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches;
  const defaultBehavior: ScrollBehavior = reduced ? 'auto' : 'smooth';
  return requested ?? defaultBehavior; // explicit prop wins
}

// usage: requested wins, otherwise system preference default
const behavior = resolveScrollBehavior(props.behavior);
```