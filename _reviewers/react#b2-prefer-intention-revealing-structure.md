---
title: Prefer intention-revealing structure
description: 'When building objects/configs or writing helper functions, prefer structures
  that clearly communicate intent and data flow.


  - Avoid “placeholder then reassigned later” patterns (e.g., creating an empty object
  and later mutating/replacing its properties). Prefer self-contained constructions
  (such as getters) so the exported shape is defined in one place.'
repository: facebook/react#b2
label: Code Style
language: TypeScript
comments_count: 2
repository_stars: 251882
---

When building objects/configs or writing helper functions, prefer structures that clearly communicate intent and data flow.

- Avoid “placeholder then reassigned later” patterns (e.g., creating an empty object and later mutating/replacing its properties). Prefer self-contained constructions (such as getters) so the exported shape is defined in one place.
- Keep exported/public types implementation-agnostic; use framework-specific types only internally for `satisfies`/validation.
- If a helper function writes into a parameter (e.g., mutating a `Set`), make that intent obvious via the signature/parameter naming—or return a value and let the caller merge.

Example (getter-based, self-contained config):
```ts
const plugin = {/* ... */};

const recommendedRuleConfigs = {/* ... */};

const configs = {
  recommended: {
    plugins: {
      get 'react-hooks'() {
        return plugin;
      },
    },
    rules: recommendedRuleConfigs,
  },
} satisfies {
  recommended: {
    plugins: Record<string, unknown>;
    rules: Record<string, unknown>;
  } };
```

Example (clarify mutation vs return):
```ts
// Prefer returning and merging, or make mutation explicit in naming.
function collectGlobalDeps(
  fn: FunctionExpression | undefined,
  outDeps: Set<IdentifierId>, // clearer than plain `deps`
): void {
  if (!fn) return;
  // ...write to outDeps
}
```