---
title: Semantic Identifier Naming
description: 'Boolean/flag and identifier names must exactly match their full meaning
  and the interop rules they participate in.


  - Name booleans by the complete predicate and user intent, not by a negated sub-condition.
  If the boolean means “show a warning because X is attached and unsupported by the
  selected model,” name it accordingly (e.g.,...'
repository: cline/cline#v21
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70886
---

Boolean/flag and identifier names must exactly match their full meaning and the interop rules they participate in.

- Name booleans by the complete predicate and user intent, not by a negated sub-condition. If the boolean means “show a warning because X is attached and unsupported by the selected model,” name it accordingly (e.g., `unsupportedImagesAttached` / `warnUnsupportedImagesAttached`), rather than `imagesUnsupported` when the expression is broader than just `!modelSupportsImages`.

- For identifiers used across components (e.g., command/menu path names), make the accepted normalization/matching behavior explicit and consistent at the boundary (e.g., `trim()` when other parts normalize). Avoid adding extra validation in one layer that isn’t enforced end-to-end; malformed names should be treated as invalid input from the source rather than “papered over” by the receiving layer.

Example (naming a boolean by its full meaning):
```ts
const modelSupportsImages = selectedModelInfo.supportsImages !== false
const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages

if (unsupportedImagesAttached) {
  // show warning / offer to switch models
}
```