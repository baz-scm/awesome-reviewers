---
title: Intent-Revealing Identifier Names
description: 'When naming variables/components, ensure identifiers encode *intent*
  and are consistent with shared conventions.


  - **Boolean/flag names must describe the situation, not just logical negation.**
  If a variable is used to trigger a warning/notice, name it accordingly.'
repository: cline/cline#v16
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70882
---

When naming variables/components, ensure identifiers encode *intent* and are consistent with shared conventions.

- **Boolean/flag names must describe the situation, not just logical negation.** If a variable is used to trigger a warning/notice, name it accordingly.
  ```ts
  // Prefer intent-based names over vague negation-like names
  const modelSupportsImages = selectedModelInfo.supportsImages !== false
  const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages
  // or: const warnUnsupportedImagesAttached = ...
  ```

- **Use consistent identifiers/imports for shared UI primitives.** If the codebase standardizes on a specific icon/component (e.g., a Lucide `X`), use that instead of ad-hoc alternatives so reviewers can quickly verify usage across the UI.
  ```tsx
  // Prefer the standard icon component import the UI package uses
  import { X } from 'lucide-react'

  <X className="h-4 w-4" />
  ```