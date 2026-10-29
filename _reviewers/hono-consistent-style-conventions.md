---
title: Consistent style conventions
description: Follow the project's established formatting conventions consistently,
  and when the linter and formatter disagree, resolve it explicitly rather than leaving
  noisy diffs or inconsistent code.
repository: honojs/hono
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 32741
---

Follow the project's established formatting conventions consistently, and when the linter and formatter disagree, resolve it explicitly rather than leaving noisy diffs or inconsistent code.

- Always use braces for conditional blocks, even single-line ones, matching the project's `curly` rule:
  ```ts
  // preferred
  if (!location) {
    return false
  }
  // avoid
  if (!location) return false
  ```
  Since `eslint-config-prettier` disables `curly`, add an explicit override in the eslint config to keep this rule enforced instead of relying on manual review.

- When ESLint and Prettier conflict (e.g. quote style with escaped apostrophes), don't just accept the clashing output—add a targeted `// eslint-disable-next-line <rule>` comment on that specific line so intent is clear and CI passes cleanly.

- Consolidate multiple imports from the same module into a single import statement, including type-only imports:
  ```ts
  // avoid
  import { parseBody } from './body'
  import type { BodyData } from './body'
  // prefer
  import { parseBody, type BodyData } from './body'
  ```
  Consider adding an ESLint rule to catch duplicate imports from the same file automatically.

- Use parentheses to make operator precedence explicit when mixing `&&`/`||` in a single condition, so the logic is unambiguous at a glance:
  ```ts
  if (contentType !== null && (contentType.startsWith('multipart/form-data') || contentType.startsWith('application/x-www-form-urlencoded'))) {
    ...
  }
  ```

- Keep semicolon/statement-start conventions consistent with the rest of the codebase (e.g., a leading `;` before a line starting with `[` or `(` in a no-semicolon codebase) rather than introducing a different pattern in new code.

Applying these conventions consistently reduces review churn, avoids CI failures from linter/formatter conflicts, and keeps the codebase readable and uniform.