---
title: Consistent Identifier Naming
description: Standardize identifier names by (1) getting spelling and renames right
  end-to-end, (2) normalizing naming at the source instead of duplicating translations,
  and (3) using consistent category-based suffix/prefix conventions for names that
  are effectively public.
repository: facebook/react#b10
label: Naming Conventions
language: JavaScript
comments_count: 5
repository_stars: 251894
---

Standardize identifier names by (1) getting spelling and renames right end-to-end, (2) normalizing naming at the source instead of duplicating translations, and (3) using consistent category-based suffix/prefix conventions for names that are effectively public.

Apply:
- **Spelling/rename safety:** When changing an identifier name (e.g., a prop), verify no lingering misspelled usage remains via repo search and update all fixtures/tests. Avoid silent fallback behavior that can mask missed renames.
  ```js
  // Before: misspelled prop name can silently fall back
  props.expectedEnviromentName || 'Server'

  // After: correct spelling, plus ensure all callers were updated
  props.expectedEnvironmentName || 'Server'
  ```
- **Normalize naming at the boundary:** If the system has multiple naming conventions (e.g., `topPress` vs `onPress`), convert once at the source and remove downstream special-casing.
  - Prefer “strip/normalize early” to “check for both names everywhere”.
- **Use consistent naming schemes by identifier category:**
  - **Options types:** Prefer consistent `${MethodName}Options`-style naming (or align with the existing convention) and don’t rename casually when the type is semi-public.
  - **Flags/categories:** Keep suffix/prefix conventions consistent within the same conceptual category (and document intentional exceptions, e.g., when no parallel render-specific flag exists).
- **Preserve public/export compatibility:** When a public name changes, keep the old export as an alias (or use a stable re-export pattern) rather than removing the old identifier or accidentally exporting `undefined`.
  ```js
  export {Activity, Activity as unstable_Activity};
  ```

Net effect: fewer silent compatibility bugs, less duplicated naming-translation logic, and clearer, more predictable naming across the codebase.