---
title: Prefer self-contained definitions
description: When defining exported objects or APIs, avoid the “initialize empty object,
  then patch/replace later” pattern. Prefer self-contained declarations (e.g., accessor/getters)
  so the final value is clear where it’s declared. Also, if a function writes into
  a passed mutable container (out-parameter), make that intent explicit—prefer returning
  a value that the...
repository: facebook/react#b1
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251878
---

When defining exported objects or APIs, avoid the “initialize empty object, then patch/replace later” pattern. Prefer self-contained declarations (e.g., accessor/getters) so the final value is clear where it’s declared. Also, if a function writes into a passed mutable container (out-parameter), make that intent explicit—prefer returning a value that the caller combines, or rename/add clarity so it’s obvious you’re mutating the argument.

Example (self-contained config with getters):
```ts
const plugin = { /* ... */ };

export const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'() {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
};
```

Example (prefer return over hidden mutation):
```ts
// Prefer returning values to avoid implicit mutation.
function getFnGlobalDeps(
  fn: FunctionExpression | undefined,
): Array<IdentifierId> {
  if (!fn) return [];
  // compute...
  return [];
}

// If you must mutate, make it explicit in naming.
function addFnGlobalDepsToSet(
  fn: FunctionExpression | undefined,
  deps: Set<IdentifierId>,
): void {
  if (!fn) return;
  // deps.add(...)
}
```