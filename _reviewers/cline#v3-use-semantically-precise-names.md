---
title: Use Semantically Precise Names
description: 'Prefer identifier names that exactly describe what the code is doing,
  and use canonical/shared identifiers when consistency matters.


  - Booleans: don’t name a flag after only part of the predicate or as a simple negation.
  If the condition includes extra context (e.g., “attachments present” plus “capability
  unsupported”), include that context in the name.'
repository: cline/cline#v3
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70863
---

Prefer identifier names that exactly describe what the code is doing, and use canonical/shared identifiers when consistency matters.

- Booleans: don’t name a flag after only part of the predicate or as a simple negation. If the condition includes extra context (e.g., “attachments present” plus “capability unsupported”), include that context in the name.

  ```ts
  // Misleading if it’s more than just “unsupported”
  const imagesUnsupported = selectedImages.length > 0 && !modelSupportsImages

  // Clear and semantic
  const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages
  // or
  const warnUnsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages
  ```

- Shared UI identifiers (icons/components): when the ecosystem already provides a standard import/component, use it so reviewers can reliably verify you’re using the same icon/primitive across the codebase (instead of custom inline SVGs that break consistency/auditability).

This improves readability, reduces misinterpretation during review, and makes intent easier to validate quickly.