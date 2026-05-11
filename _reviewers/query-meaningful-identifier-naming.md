---
title: Meaningful Identifier Naming
description: Use names that clearly reflect the thing being identified, and ensure
  renamed identifiers don’t accidentally couple to old data or misleading conventions.
repository: tanstack/query
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 49380
---

Use names that clearly reflect the thing being identified, and ensure renamed identifiers don’t accidentally couple to old data or misleading conventions.

- **When an identifier backs persisted/external state (e.g., `localStorage` keys), rename the storage key as well** to prevent reusing stale values after refactors.

  ```ts
  // Before: reads old stored values
  const [sortDesc, setSortDesc] = useLocalStorage('reactQueryDevtoolsSortDesc', '')

  // After: new state name, use a new storage key
  const [baseSort, setBaseSort] = useLocalStorage('reactQueryDevtoolsBaseSort', '')
  ```

- **Name test files/identifiers for the specific scenario being tested; avoid redundant labels** when the suffix/extension already implies the category.

  ```txt
  # Prefer a scenario/feature name
  mutations.test-d.tsx
  ```

Applying this keeps naming semantically aligned with behavior and prevents accidental cross-contamination from previously persisted names.