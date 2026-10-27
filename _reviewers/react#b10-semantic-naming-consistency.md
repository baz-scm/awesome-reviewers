---
title: Semantic Naming Consistency
description: 'When naming (handwritten or generated), optimize for semantic clarity
  and consistency: don’t introduce needless renames, preserve meaningful existing
  names, and use a stable vocabulary across related APIs.'
repository: facebook/react#b10
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251894
---

When naming (handwritten or generated), optimize for semantic clarity and consistency: don’t introduce needless renames, preserve meaningful existing names, and use a stable vocabulary across related APIs.

Guidelines:
1) Avoid needless renames; prefer idiomatic patterns
- Use shorthand destructuring when possible.
- Quote keys when the source property name doesn’t match the identifier you want (e.g. kebab-case).

```js
// Prefer
const { disabled, 'aria-label': ariaLabel } = props;

// Avoid renaming that doesn’t add meaning
const { disabled: disabled, ariaLabel: ariaLabel } = props;
```

2) Keep terminology consistent across the surface area
- If the concept is the same, use the same core term everywhere; only add suffixes/prefixes to reflect real differences in returned data shape.

3) Preserve original meaningful function/variable names
- Only rename or wrap when the original name is truly anonymous/unknown; don’t rewrite names that already carry intent.

4) For generated identifiers, apply framework-aware simplification rules
- Don’t bake in redundant indices (e.g. `arg0`) when framework conventions indicate it’s unnecessary (e.g. certain React built-in hook cases). Ensure the rule is consistent and documented in the code generation logic.

Applying this keeps naming predictable for humans, reduces noise in diffs, and makes tool outputs and generated code easier to understand and maintain.