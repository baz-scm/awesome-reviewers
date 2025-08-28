---
title: eliminate redundant null checks
description: Remove unnecessary null/undefined checks when you already have sufficient
  validation in place, and use proper type guards instead of type assertions for better
  null safety.
repository: cloudflare/workers-sdk
label: Null Handling
language: TypeScript
comments_count: 3
repository_stars: 3379
---

Remove unnecessary null/undefined checks when you already have sufficient validation in place, and use proper type guards instead of type assertions for better null safety.

When you've already validated that a value is truthy or non-null, avoid redundant checks that add noise without providing additional safety. Similarly, prefer type guard functions over type assertions to maintain proper null safety.

Examples of improvements:
- If you have `if (match)` then `const [, year, month, date] = match` is sufficient - no need for `match ?? []`
- Instead of checking both `response instanceof UndiciResponse && !(response instanceof Response)`, determine which single check provides the necessary validation
- Replace type assertions like `(newModule as Record<string, unknown>)` with proper type guard functions that can handle null/undefined cases safely

This approach reduces code complexity while maintaining robust null handling, making your code both cleaner and safer.