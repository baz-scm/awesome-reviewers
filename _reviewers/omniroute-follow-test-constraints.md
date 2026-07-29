---
title: Follow test constraints
description: 'When adding UI logic or tests, align with the repository’s existing
  CI/test guardrails—especially global checks and test discovery conventions.


  - **Respect cross-cutting test rules (e.g., i18n parity):** Don’t introduce changes
  that require mass updates across all locales/fixtures unless you’re prepared to
  complete them. If full compliance is out of scope,...'
repository: diegosouzapw/OmniRoute
label: Testing
language: TSX
comments_count: 2
repository_stars: 33162
---

When adding UI logic or tests, align with the repository’s existing CI/test guardrails—especially global checks and test discovery conventions.

- **Respect cross-cutting test rules (e.g., i18n parity):** Don’t introduce changes that require mass updates across all locales/fixtures unless you’re prepared to complete them. If full compliance is out of scope, keep the functional change minimal and defer complete i18n work to a focused follow-up.
- **Follow existing test organization/discovery patterns:** Place new tests where Vitest/CI already expects them (e.g., co-located `__tests__` for dashboard components if the repo’s `vitest.config.ts` includes that path). Avoid reorganizing test locations unless you also update imports and discovery configuration.

Example (i18n guardrail pattern):
```tsx
// Prefer keeping the diff focused when full i18n key rollout is out of scope.
{condition && (
  // Inline callout instead of adding en-only keys that break locale-parity tests.
  <div className="text-xs">...</div>
)}
// Then open a follow-up PR to properly add i18n keys across required locales.
```

Example (test structure pattern):
```ts
// Keep dashboard component tests co-located under the component's __tests__
// so existing Vitest include globs discover them consistently.
// Put your new *.test.tsx next to the component tests rather than in a different folder
// unless the repo-wide convention is being intentionally changed.
```