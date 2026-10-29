---
title: Prefer concise idiomatic syntax
description: 'Write code using the shortest, most idiomatic form that remains clear,
  and stay consistent with the project''s established conventions rather than reverting
  to verbose patterns. Concretely:'
repository: HONOJS/HONO
label: Code Style
language: TypeScript
comments_count: 10
repository_stars: 32741
---

Write code using the shortest, most idiomatic form that remains clear, and stay consistent with the project's established conventions rather than reverting to verbose patterns. Concretely:

- Use shorthand object properties instead of repeating keys: `{ path, method, handler }` rather than `{ path: path, method: method, handler: handler }`.
- Use optional chaining and nullish coalescing to collapse verbose conditional returns, e.g. `return opt?.after?.(await res) ?? res` instead of multi-branch if/else.
- Always wrap single-statement control-flow bodies in braces (`if (!x) { return false }`) to match the project's `curly` lint rule; don't rely on single-line `if` statements.
- Avoid introducing unnecessary async IIFEs or wrapper functions just to scope a few lines — restructure with early returns/`switch` blocks instead.
- When the same block of logic (e.g. building a response/headers) is duplicated more than once in a file, extract it into a single named helper function rather than copy-pasting.
- Favor simpler, well-known patterns for transformations (e.g. a single regex for camelCase→kebab-case conversion) over hand-rolled multi-branch logic, when they are equally correct and more readable.
- When combining `&&`/`||` in a single condition, use parentheses to make operator precedence and intent explicit, e.g. `contentType !== null && (contentType.startsWith('a') || contentType.startsWith('b'))`.
- Keep statement-termination style (semicolons vs. ASI) consistent with the rest of the file/codebase; if the codebase omits semicolons, use a leading `;` only when required to disambiguate a new statement.

The goal is code that a reviewer can scan quickly: no redundant boilerplate, no accidental ambiguity from operator precedence or missing braces, and no duplicated logic scattered across a file.