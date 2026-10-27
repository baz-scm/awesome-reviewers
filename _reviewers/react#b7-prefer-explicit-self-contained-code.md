---
title: Prefer explicit self-contained code
description: When defining configuration objects or helper APIs, avoid patterns that
  hide intent (e.g., placeholder objects that get reassigned later, or parameters
  used only as output). Write code so the final shape is declared directly and data
  flow is clear.
repository: facebook/react#b7
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251888
---

When defining configuration objects or helper APIs, avoid patterns that hide intent (e.g., placeholder objects that get reassigned later, or parameters used only as output). Write code so the final shape is declared directly and data flow is clear.

**1) Use accessors/getters for computed mappings instead of placeholder+reassign**
Avoid “create empty object, then later assign into it” for exported config maps. Prefer an accessor/getter so the mapping is self-contained.

```ts
const plugin = { /* ... */ };

const recommended = {
  plugins: {
    get 'react-hooks'(): ESLint.Plugin {
      return plugin;
    },
  },
  rules: recommendedRuleConfigs,
};
```

**2) Don’t leak implementation types in exported types**
If you need `ESLint.Plugin` (or similar) for correctness, keep it internal (e.g., via `satisfies`) rather than baking it into publicly exported type shapes.

**3) Prefer return values over “output parameters”**
For helpers that collect results (like writing into a `Set`/`deps`), prefer returning the collected data. If you must mutate a passed-in collection, make the “this is an output” intent obvious in the signature/name/documentation.

```ts
// Prefer:
function getFnGlobalDeps(fn: FunctionExpression | undefined): IdentifierId[] {
  const deps: IdentifierId[] = [];
  // ...collect...
  return deps;
}

// Or if mutating:
function collectFnGlobalDeps(
  fn: FunctionExpression | undefined,
  outDeps: Set<IdentifierId>,
): void {
  // ...write into outDeps...
}
```