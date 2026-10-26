---
title: Meaningful Naming Consistency
description: Use names that are semantically correct, consistent across APIs, and
  preserve developer intent. Prefer minimal renames—only change names when required
  for correctness (e.g., special-character property keys) or to avoid ambiguity (e.g.,
  anonymous vs named functions, or when a term describes a specific data shape).
repository: facebook/react#b3
label: Naming Conventions
language: Markdown
comments_count: 3
repository_stars: 251883
---

Use names that are semantically correct, consistent across APIs, and preserve developer intent. Prefer minimal renames—only change names when required for correctness (e.g., special-character property keys) or to avoid ambiguity (e.g., anonymous vs named functions, or when a term describes a specific data shape).

Do:
- **Use minimal, standard naming transformations** (avoid redundant renames). 
  ```js
  // Prefer shorthand destructuring
  const { disabled, 'aria-label': ariaLabel } = props;
  ```
- **Match terminology to meaning and return shape**; don’t reuse a term for different concepts.
  - If you’re returning an owner “stack” trace, keep “stack/trace” in the name; if you return a different structure (e.g., an ordered owner list/branch), use a distinct suffix/name.
- **Preserve explicit identifier names** when they were originally provided by the author; only wrap/rename when the original function was truly anonymous and would otherwise become unclear.

Don’t:
- Rename `x: x` when shorthand `x` is clearer.
- Change `aria-label` handling into a camelCase key unless you’re also changing the actual prop contract.
- Use the same label (e.g., “stack” vs “branch”) for different returned structures without naming differences that reflect the real shape/behavior.