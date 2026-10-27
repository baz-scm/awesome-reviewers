---
title: Consistent Naming Standards
description: 'Adopt naming rules that keep identifiers (and generated labels) semantically
  clear, consistent, and minimally noisy.


  Do:

  - Use clear destructuring names:'
repository: facebook/react#b4
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251885
---

Adopt naming rules that keep identifiers (and generated labels) semantically clear, consistent, and minimally noisy.

Do:
- Use clear destructuring names:
  - Prefer shorthand when renaming isn’t needed.
  - Quote destructuring keys when the property name isn’t a valid identifier (e.g., `aria-label`).
  - Example:
    ```js
    // good
    const { disabled, 'aria-label': ariaLabel } = props;
    // avoid
    const { disabled: disabled, ariaLabel: ariaLabel } = props;
    ```
- Keep established domain terminology consistent in APIs/tools. If names imply a meaning (e.g., “stack”), don’t overload them for different return shapes—encode the difference in the tool name (e.g., add an explicit suffix like “stack_trace” vs “stack”).
- Minimize unnecessary naming noise in generated identifiers/labels:
  - Special-case well-known patterns so labels don’t carry redundant data (e.g., avoid `arg0` in hook-related labels when it would be dropped for built-in hooks).
- Preserve meaningful existing names: don’t rename/wrap functions unless they are truly anonymous constructs requiring transformation.

In practice: when you touch naming—whether for hand-written code or compiler-generated labels—opt for the most stable, domain-accurate term, remove redundancy, and preserve original meaning when it already exists.