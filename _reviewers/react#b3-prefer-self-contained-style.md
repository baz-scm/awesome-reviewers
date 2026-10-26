---
title: Prefer self-contained style
description: When building exported configuration objects or APIs, avoid “placeholder
  then overwrite” patterns that obscure intent. Prefer self-contained construction
  (e.g., direct object literals or getters/accessors for lazily-provided values) so
  the source of each field is obvious, and keep exported types framework-agnostic.
repository: facebook/react#b3
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251883
---

When building exported configuration objects or APIs, avoid “placeholder then overwrite” patterns that obscure intent. Prefer self-contained construction (e.g., direct object literals or getters/accessors for lazily-provided values) so the source of each field is obvious, and keep exported types framework-agnostic.

Apply:
- For exported config objects: don’t create an empty object and later reassign/augment it; instead construct the final shape directly or expose values via getters.
- For typings: validate structure with `satisfies` rather than embedding framework-specific types in exported type aliases.
- For functions: make it explicit whether you return data or mutate a provided collection; choose either “return an array for merging” or clearly communicate that the argument is an output (e.g., naming/structure).

Example (getter-based config to keep intent local):
```ts
const plugin = { /* ... */ } satisfies Record<string, unknown>;

const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'(): ESLint.Plugin {
        return plugin as ESLint.Plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
};
```

Example (clarify return vs mutation):
```ts
function collectGlobalDeps(fn: FunctionExpression | undefined): IdentifierId[] {
  const deps: IdentifierId[] = [];
  if (!fn) return deps;
  // push into deps...
  return deps;
}
```