---
title: Use Intentful Naming
description: When introducing variables, flags, or UI primitives, ensure the name
  matches the *full intent/semantics* and follows the project’s established naming/pattern
  conventions.
repository: cline/cline#v24
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70891
---

When introducing variables, flags, or UI primitives, ensure the name matches the *full intent/semantics* and follows the project’s established naming/pattern conventions.

- **Boolean/flag naming must describe the actual condition**, not just one sub-check.
  - Bad pattern: a name implying only “unsupported” when the value also depends on “something is attached”.
  - Prefer names that encode the *trigger* clearly.

  ```ts
  // Prefer names that capture the full predicate semantics
  const modelSupportsImages = selectedModelInfo.supportsImages !== false
  const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages
  const warnUnsupportedImagesAttached = unsupportedImagesAttached
  ```

- **Use canonical/shared identifiers for UI primitives** so intent is easy to verify.
  - Prefer the standard icon/component import pattern (e.g., from `lucide`) rather than inline duplicated SVG markup, which makes it harder to confirm consistency.

Applying this keeps code search, reviews, and future maintenance aligned: names communicate meaning, and shared primitives preserve consistency across the codebase.