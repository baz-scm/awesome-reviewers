---
title: Client API Semantics
description: 'When designing client-side “API” surfaces (REST-derived client decisions
  and reusable UI component props), make semantics explicit and deterministic:

  '
repository: cline/cline#v13
label: API
language: TSX
comments_count: 2
repository_stars: 70874
---

When designing client-side “API” surfaces (REST-derived client decisions and reusable UI component props), make semantics explicit and deterministic:

- Use a single source of truth for client decisions. If the client can derive the correct behavior from local/provider state, avoid adding or reintroducing server lookups that duplicate logic or change failure/behavior modes.
- Treat ambient/system conditions (e.g., `prefers-reduced-motion`) as defaults, not hard-coded behavior. Define precedence clearly: **ambient default < explicit prop override**.
- Lock the precedence/behavior with tests so future refactors don’t silently change semantics.

Example pattern (ambient default with prop override):
```ts
function resolveScrollBehavior({ behavior }: { behavior?: 'auto' | 'smooth' }) {
  const reduced = window.matchMedia?.('(prefers-reduced-motion: reduce)')?.matches;
  const ambientDefault: 'auto' | 'smooth' = reduced ? 'auto' : 'smooth';
  return behavior ?? ambientDefault; // explicit prop wins
}

// Similar idea: decide which model/provider to use from local provider state
// rather than calling a plan endpoint when the client already knows which models
// are applicable and how failures should surface.
```

Apply this to both (a) endpoints/data dependencies used to choose client behavior and (b) reusable UI component props that encapsulate behavior.