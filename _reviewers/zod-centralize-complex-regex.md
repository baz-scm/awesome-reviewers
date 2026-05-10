---
title: Centralize Complex Regex
description: 'When adding validation logic that uses complex literals (especially
  RegExp), keep it consistent and maintainable:


  - Don’t scatter regex literals inline across files/branches—move them to a shared
  constant block near other related regexes.'
repository: colinhacks/zod
label: Code Style
language: TypeScript
comments_count: 7
repository_stars: 42628
---

When adding validation logic that uses complex literals (especially RegExp), keep it consistent and maintainable:

- Don’t scatter regex literals inline across files/branches—move them to a shared constant block near other related regexes.
- If the regex is too complex to be readable/reviewable, extract it into a named helper (e.g., `isValidIpv6`) so the parsing/intent is clear.
- Reuse the centralized constant/helper everywhere in the module; avoid creating unused helpers.
- If eslint/linter requires suppression for regex style, prefer refactoring to satisfy the linter, and only use `eslint-disable` when behavior is unchanged and the suppression is clearly justified.

Example (centralizing a slug regex):

```ts
// Regex constants near other regexes
const slugRegex = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

export function isSlug(value: string): boolean {
  return slugRegex.test(value);
}

// Reuse in validation instead of repeating the literal
// if (check.kind === "slug") { ... slugRegex ... }
```

This improves readability, reduces review/merge churn, and makes future tweaks to validation patterns less error-prone.