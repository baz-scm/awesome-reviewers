---
title: JSX runtime compatibility
description: When building or extending a JSX/React-compatible module, aim for full
  conformance with the standard JSX/React behavior rather than a partial subset, so
  consumers (and tools built on top, like HonoX) can rely on familiar APIs and correct
  rendering semantics.
repository: honojs/Hono
label: React
language: TypeScript
comments_count: 2
repository_stars: 32741
---

When building or extending a JSX/React-compatible module, aim for full conformance with the standard JSX/React behavior rather than a partial subset, so consumers (and tools built on top, like HonoX) can rely on familiar APIs and correct rendering semantics.

- Export the complete, conventional API surface expected from a JSX runtime or compatibility layer (e.g. `jsx`, `createElement`, hooks like `useState`/`useEffect`, etc.), matching what the equivalent module (e.g. `hono/jsx`) already exports, even if a given export isn't strictly required for the primary use case. This avoids surprising gaps for consumers who import from `*/jsx-runtime` or rely on parity with React's API.
- When rendering JSX attributes to HTML, correctly special-case all HTML boolean attributes (not just a couple), e.g. `checked`, `selected`, `disabled`, `readonly`, `multiple`. A boolean attribute set to `false` must be omitted entirely rather than rendered as `attr="false"`:

```ts
const booleanAttributes = ['checked', 'selected', 'disabled', 'readonly', 'multiple']

if (booleanAttributes.includes(propsKeys[i]) && v === false) {
  continue // omit the attribute instead of rendering "false"
}
```

Treat JSX/React compatibility as an explicit contract: verify exports and attribute-handling behavior against the HTML/React spec before merging, and extend coverage (exports or attribute lists) whenever a gap is found.</description>
</invoke>
