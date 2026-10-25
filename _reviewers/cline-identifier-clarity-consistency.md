---
title: Identifier clarity & consistency
description: 'Use naming that precisely describes meaning (especially booleans/flags)
  and keep externally-relevant identifiers/assets consistent across call sites.

  '
repository: CLINE/cline
label: Naming Conventions
language: TSX
comments_count: 3
repository_stars: 70839
---

Use naming that precisely describes meaning (especially booleans/flags) and keep externally-relevant identifiers/assets consistent across call sites.

Apply these rules:
1) **Name booleans for the full condition they represent**
- Don’t name a flag after only one part of the logic if it includes additional constraints.
- Example (better):
```ts
const modelSupportsImages = selectedModelInfo.supportsImages !== false
const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages
// or: const warnUnsupportedImagesAttached = unsupportedImagesAttached
```

2) **Normalize/format identifiers the same way across boundaries**
- If a command/menu path is normalized (e.g., trimming) before inspection/display, apply the same normalization wherever it’s compared or surfaced.
- Avoid “papering over” malformed identifiers by adding special-case validation unless the system contract requires it.

3) **Use consistent UI component/imports for shared elements**
- Prefer the same icon component/import pattern across the codebase so reviewers can quickly verify visual/semantic consistency (e.g., using the shared Lucide icon component rather than ad-hoc inline markup when the project standard exists).