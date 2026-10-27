---
title: Explicit Public API Shapes
description: 'When adding or modifying public (exported) APIs, make the call shape
  explicit and future-proof:


  - Prefer an **options bag / keyed arguments object** for extensible parameters,
  so new fields can be added without breaking positional call patterns.'
repository: facebook/react#b14
label: API
language: JavaScript
comments_count: 5
repository_stars: 251893
---

When adding or modifying public (exported) APIs, make the call shape explicit and future-proof:

- Prefer an **options bag / keyed arguments object** for extensible parameters, so new fields can be added without breaking positional call patterns.
- Clearly model **required vs optional** inputs in public type signatures. If a field might be omitted by a future implementation (and it’s public), make it optional now.
- Use **correct generic variance and optionality** so consumer code composes safely (e.g., `Store<Dog>` is usable where `Store<Animal>` is expected).

Example (typed, variance-aware store API):

```js
// Prefer explicit generic variance + optional reducer action typing
export type ReactStore<+Value, -Action = empty> = {
  $$typeof: symbol,
  _current: Value,
  _sync: Value,
  _transition: Value,
};

export function createStore<Value, Action = empty>(
  defaultValue: Value,
  reducer?: (value: Value, action?: Action) => Value,
): ReactStore<Value, Action> {
  // ...
}
```

Practical checklist:
- Can new parameters be added without changing positional arguments? (If not, switch to an options bag.)
- Do public types accurately reflect what callers can/must provide? (Required vs optional.)
- Do exported generics use variance so type assignments work naturally for consumers?