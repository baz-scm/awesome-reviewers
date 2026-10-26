---
title: Name flags precisely
description: 'When naming variables/props/identifiers, ensure the name matches the
  exact semantic meaning and the project’s established identity conventions.


  Apply:'
repository: cline/cline#v11
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70871
---

When naming variables/props/identifiers, ensure the name matches the exact semantic meaning and the project’s established identity conventions.

Apply:
- Boolean flags: name should describe the full predicate, not only a sub-condition.
  - Bad (implies only capability-based unsupportedness):
    ```ts
    const imagesUnsupported = selectedImages.length > 0 && !modelSupportsImages
    ```
  - Better (describes the additional dependency):
    ```ts
    const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages
    ```
- Shared UI primitives: prefer the standard imported component/identifier for known icons/buttons so reviewers can quickly verify consistency across the codebase.
  - Bad: inline SVG for a known “X/close” icon.
  - Better: use the shared icon component (e.g., from your standard lucide wrapper) with consistent props.

If a value’s meaning depends on more than one factor (capability + user action, etc.), include that in the name—or choose a name that’s clearly broader than a single underlying condition.