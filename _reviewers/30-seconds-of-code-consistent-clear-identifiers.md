---
title: Consistent, Clear Identifiers
description: 'Use naming that is consistent with the surrounding code/style, avoids
  ambiguity, and preserves semantic meaning—both in code and in documentation.


  Rules:'
repository: 30-seconds/30-seconds-of-code
label: Naming Conventions
language: Markdown
comments_count: 5
repository_stars: 129334
---

Use naming that is consistent with the surrounding code/style, avoids ambiguity, and preserves semantic meaning—both in code and in documentation.

Rules:
- Match the existing naming convention (e.g., Python snippet uses lowercase variable names):
  - Prefer `sum` over `Sum` when the rest is `snake_case`/lowercase.
- Avoid shadowing/ambiguity:
  - Don’t use the same identifier for a collection and the iterated element.
  - Example:
    ```js
    a.forEach((value) => { magnitudeOfA += value ** 2; });
    ```
- Prefer readability over excessive abbreviation:
  - Use clearer names like `length` instead of vague short forms.
- When transforming casing (title case, etc.), don’t destroy internal capital patterns (e.g., `mcDolans` should not become `Mcdolans`).
- When referencing built-ins in text/docs, use canonical API names:
  - Use `Array.prototype.map()` (not just `map()`).