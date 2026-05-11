---
title: Configurable tooling rules
description: Specialized tooling (lint rules, dev-only packages, docs navigation)
  must be explicitly enabled and driven by configuration so it won’t misfire in the
  wrong project context.
repository: tanstack/query
label: Configurations
language: Markdown
comments_count: 3
repository_stars: 49380
---

Specialized tooling (lint rules, dev-only packages, docs navigation) must be explicitly enabled and driven by configuration so it won’t misfire in the wrong project context.

Apply this standard:
- Lint rules: avoid broad directory/name heuristics. Make framework/server-specific checks opt-in, or allow configuration of the directories/files the rule applies to.
- Dev-only bundles: gate development tools with environment flags (e.g., only include devtools when `NODE_ENV === 'development'`).
- Docs/UX surfaces: when adding new docs pages/features, update the relevant config sources (e.g., `docs/config.json`) so the change is actually discoverable.

Example (lint applicability via opt-in/config):
```js
// eslint.config.js (example approach)
export default [
  {
    // Only run the SSR-specific rule for explicitly configured Next.js entrypoints
    rules: {
      '@tanstack/query/no-module-query-client': ['error', { enabled: true }],
    },
    files: [
      '**/pages/_app.{js,jsx,ts,tsx}',
      '**/pages/_document.{js,jsx,ts,tsx}',
      '**/app/_app.{js,jsx,ts,tsx}',
      '**/app/_document.{js,jsx,ts,tsx}',
    ],
  },
]
```

Example (env-gated devtools):
```ts
// Only include devtools in development bundles
if (process.env.NODE_ENV === 'development') {
  // import/load devtools
}
```