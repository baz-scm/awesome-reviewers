---
title: Consistent Minimal Naming
description: 'When naming variables, destructured fields, public tools, or generated/transformed
  identifiers, apply these rules:


  - **Avoid redundant renames:** prefer shorthand/descriptive bindings instead of
  renaming to the same meaning.'
repository: facebook/react#b5
label: Naming Conventions
language: Markdown
comments_count: 4
repository_stars: 251886
---

When naming variables, destructured fields, public tools, or generated/transformed identifiers, apply these rules:

- **Avoid redundant renames:** prefer shorthand/descriptive bindings instead of renaming to the same meaning.
  ```js
  // Bad: redundant rename
  const { disabled: disabled, 'aria-label': ariaLabel } = props;

  // Good: shorthand
  const { disabled, 'aria-label': ariaLabel } = props;
  ```
- **Quote keys that aren’t valid identifiers:** for props/object keys like `aria-label`, use a quoted destructuring key.
- **Keep core terminology stable; disambiguate with suffixes:** if two things share a concept but return different shapes, retain the shared term and add a targeted suffix rather than swapping the core word.
  ```txt
  react_get_owners_stack        // owner stack list
  react_get_owners_stack_trace  // trace frames
  ```
- **Preserve existing names; only add qualifiers when necessary:**
  - If a function already has a meaningful name, keep it.
  - If it’s truly anonymous, name it deterministically, but **minimize noise** (e.g., don’t emit `arg0`-style labels when the context already makes the meaning unambiguous; add indices only when multiple candidates exist).

Follow this checklist during reviews to ensure names are readable, consistent across the codebase/API surface, and not cluttered with unnecessary renames or boilerplate qualifiers.