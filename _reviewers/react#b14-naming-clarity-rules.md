---
title: Naming Clarity Rules
description: "Adopt naming that is semantically accurate, consistent, and avoids needless\
  \ noise.\n\n- Prefer the simplest correct identifier form.\n  - Example (destructuring):"
repository: facebook/react#b14
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251893
---

Adopt naming that is semantically accurate, consistent, and avoids needless noise.

- Prefer the simplest correct identifier form.
  - Example (destructuring):
    ```js
    // Prefer shorthand when key and local name match
    const { disabled } = t0;

    // For dashed keys, keep the key correct and quote it
    const { 'aria-label': ariaLabel } = t0;
    ```
- Use stable terminology for the same concept/type; don’t switch terms when shapes differ.
  - If you have both a raw “stack” (frames) and a structured “branch” (owners list), make the names reflect that distinction (e.g., `..._stack_trace` vs `..._stack`).
- Preserve existing meaningful names and only rename when you must.
  - Don’t rename intentional function declarations just because you’re transforming nearby anonymous wrappers; only generate/rename when the source identifier is truly anonymous and needs disambiguation.
- Minimize index/arg noise in generated identifiers.
  - Only include indices when necessary for uniqueness (e.g., when multiple anonymous arguments would otherwise collide); otherwise prefer a cleaner name.