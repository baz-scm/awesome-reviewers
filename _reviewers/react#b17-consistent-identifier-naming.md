---
title: Consistent Identifier Naming
description: 'Use names that are semantically accurate, consistent across the surface
  area (APIs/tools/generated output), and minimally aliased.


  Apply these rules:'
repository: facebook/react#b17
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251891
---

Use names that are semantically accurate, consistent across the surface area (APIs/tools/generated output), and minimally aliased.

Apply these rules:
- **Avoid unnecessary renames/aliasing**: when destructuring or transforming, prefer stable keys and shorthand rather than manufacturing redundant local identifiers.
  ```js
  // Prefer shorthand + correct key spelling
  const { disabled, 'aria-label': ariaLabel } = props;
  ```
- **Preserve meaningful original names**: only synthesize/rename when the input truly lacks a stable name (e.g., an anonymous function assigned to a variable). If a function already has a meaningful name, keep it.
- **Keep terminology consistent and unambiguous**: don’t introduce competing terms for related concepts (e.g., use `stack` consistently). If two return shapes differ, reflect that via clear suffixes rather than changing the primary term.
  - Example pattern: `react_get_owners_stack_trace` vs `react_get_owners_stack`.
- **Minimize redundant identifier noise in generated output**: avoid adding extra “index” detail when it isn’t necessary to distinguish semantics (e.g., keep built-in hook argument naming compact when only one form applies).

Result: identifiers remain readable, stable, and predictable—making both human debugging and automated comparison easier.