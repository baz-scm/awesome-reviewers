---
title: Consistent readable patterns
description: "Apply consistent, type-safe idioms and keep logic/formatting easy to\
  \ scan.\n\n- Prefer the established guard/pattern style:\n  ```ts\n  // preferred\
  \ if the surrounding code uses boolean guards"
repository: tanstack/query
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 49380
---

Apply consistent, type-safe idioms and keep logic/formatting easy to scan.

- Prefer the established guard/pattern style:
  ```ts
  // preferred if the surrounding code uses boolean guards
  theme && devtools.setTheme(theme)
  ```
- Remove redundant casts like `as any` when TypeScript can infer/narrow:
  ```ts
  const options = query.options // avoid unnecessary `as any`
  ```
- Extract and reuse common “value or function” handling instead of repeating `typeof ... === 'function'` checks; use shared helpers (e.g., a `resolveValueOrFunction` utility) across the codebase.
- Keep control flow structured: avoid duplicated assignments/notifications and hard-to-follow early returns. Split logic by the primary conditions (e.g., index change vs result change), then assign/notify accordingly.
- Enforce consistent formatting/import conventions (grouping, ordering, quote style) to reduce diff noise and improve readability.

Use these guidelines to guide refactors during reviews, not only new code.