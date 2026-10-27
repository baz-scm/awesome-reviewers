---
title: Readable, Typed Code Style
description: Prefer code style that is explicit, readable, and type-correct—minimize
  redundant comments and unnecessary conditional checks, use consistent JS equality/helpers,
  and avoid `FlowFixMe` when proper typings are straightforward.
repository: facebook/react#b11
label: Code Style
language: JavaScript
comments_count: 8
repository_stars: 251894
---

Prefer code style that is explicit, readable, and type-correct—minimize redundant comments and unnecessary conditional checks, use consistent JS equality/helpers, and avoid `FlowFixMe` when proper typings are straightforward.

Practical rules:
- Use strict equality by default: prefer `===` over `==` unless a specific weak-equality requirement exists.
- Don’t add comments that restate what the code obviously does; remove “obvious intent” comments when they don’t add information.
- Avoid unnecessary “isX(...)” branches when control flow already guarantees the condition—structure helpers/switches so the guaranteed case is handled directly.
- Prefer proper Flow typings over `// $FlowFixMe[missing-...]` for callback parameters; only use Flow escapes intentionally and annotate them clearly.
- Keep control flow readable: avoid multiline ternaries for branching logic; use `if`/early returns where clarity improves.
- Use shared helpers for consistency (and Flow reasons) rather than duplicating equivalent platform checks.

Example (multiline ternary → if):
```js
// Bad (hard to scan)
return condition ? a : b;

// Good
if (condition) {
  return a;
}
return b;
```

Example (avoid unnecessary FlowFixMe by typing):
```js
// Bad
// $FlowFixMe[missing-local-annot]
function onChange({currentTarget}) {
  currentTarget.select();
}

// Good
type CurrentTarget = HTMLInputElement;
function onChange({currentTarget}: {currentTarget: CurrentTarget}) {
  currentTarget.select();
}
```

Example (strict equality):
```js
if (key === __PROTO__) {
  return undefined;
}
```