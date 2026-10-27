---
title: Prefer self-contained config
description: When building exported config structures or helper APIs, choose patterns
  that are self-contained, intention-revealing, and avoid unnecessary coupling.
repository: facebook/react#b8
label: Code Style
language: TypeScript
comments_count: 3
repository_stars: 251889
---

When building exported config structures or helper APIs, choose patterns that are self-contained, intention-revealing, and avoid unnecessary coupling.

Apply:
1) Avoid “empty object then reassign/mutate” for exported configs. Prefer lazy/self-contained accessors so the final shape is produced directly.
2) Don’t expose implementation/external library types in exported type definitions unless required. Validate with `satisfies` instead.
3) Make helper write/side effects obvious (prefer returning a value, or name out-params clearly). Also avoid mixing different approaches (e.g., typing + dataflow) when one mechanism suffices—keep logic based on a single source of truth.

Example (self-contained config via getter):
```ts
const plugin = /* ... */;

const config = {
  recommended: {
    plugins: {
      get 'react-hooks'(): ESLint.Plugin {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
} satisfies {
  recommended: {
    plugins: { [key: string]: unknown };
    rules: Record<string, unknown>;
  };
```

If you need a helper to accumulate results, either return the collection:
```ts
function getGlobalDeps(fn: FunctionExpression | undefined): Array<IdentifierId> {
  // ...
}
```

…or make the side-effect explicit in naming/signature:
```ts
function collectGlobalDeps(fn: FunctionExpression | undefined, deps: Set<IdentifierId>): void {
  // ...
}
```