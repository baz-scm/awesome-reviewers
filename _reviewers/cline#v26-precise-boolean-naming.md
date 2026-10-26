---
title: Precise Boolean Naming
description: When naming boolean flags (and other identifiers derived from multiple
  inputs), make the name reflect the *exact condition* being tested—not a vague negation
  of another variable.
repository: cline/cline#v26
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70893
---

When naming boolean flags (and other identifiers derived from multiple inputs), make the name reflect the *exact condition* being tested—not a vague negation of another variable.

Concretely:
- If the boolean represents a composite state (e.g., “attachments exist” AND “capability says unsupported”), the name should include that composite intent.
- Avoid names that imply only one part of the logic (e.g., “`imagesUnsupported`” when the actual meaning is “unsupported images are attached and should warn”).

Example (adapted from the pattern discussed):
```ts
const modelSupportsImages = selectedModelInfo.supportsImages !== false;
const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages;

if (unsupportedImagesAttached) {
  // show badge/notice
}
```

As a related consistency practice, ensure identifier-bearing values are normalized so the same “meaning” is preserved across boundaries (e.g., trimming menu paths to match internal normalization).