---
title: Concise Semantic Naming
description: Code should follow naming rules that preserve meaning, avoid redundancy,
  and use idiomatic identifier transformations—especially when rewriting/normalizing
  function and prop names.
repository: facebook/react#b8
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 251889
---

Code should follow naming rules that preserve meaning, avoid redundancy, and use idiomatic identifier transformations—especially when rewriting/normalizing function and prop names.

Apply these rules:

1) Use idiomatic destructuring for prop/field names
- Prefer shorthand when renaming isn’t needed:
  ```js
  const { disabled, 'aria-label': ariaLabel } = t0;
  ```
- Quote destructuring keys that aren’t valid identifiers (e.g., hyphenated props like `aria-label`).

2) Preserve existing meaningful function names
- Don’t rename/wrap functions that are already named.

3) Name or wrap only true anonymous-as-assigned functions
- If an inner function originates as an anonymous function assigned to a variable/property, generate a stable derived name so references remain clear.
- If the function already had a name, keep it as-is.

4) Keep hook-related naming minimal
- For built-in React effect hooks, avoid redundant argument indices in identifiers/keys when they don’t add disambiguation (e.g., prefer `Component[useEffect]` over `Component[useEffect(arg0)]`).
- Only include an argument index when multiple anonymous function arguments require disambiguation.

Result: names remain semantically stable, syntax is correct/idiomatic, and generated identifiers are concise without losing meaning.