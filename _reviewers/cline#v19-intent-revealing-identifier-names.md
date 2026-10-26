---
title: Intent-Revealing Identifier Names
description: When naming variables (especially booleans), ensure the name describes
  the *user-visible intent/state* of the computed value—not just the raw predicate
  or the negation of another flag. If the value implies a warning/notice or covers
  a broader condition, encode that in the name.
repository: cline/cline#v19
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 70885
---

When naming variables (especially booleans), ensure the name describes the *user-visible intent/state* of the computed value—not just the raw predicate or the negation of another flag. If the value implies a warning/notice or covers a broader condition, encode that in the name.

Also, ensure the data you expose via these identifiers is semantically consistent with the canonical producer/consumer (e.g., normalize strings/paths to match the runner or external system), so the identifier’s meaning stays stable across boundaries.

Examples:
```ts
// ❌ Misleading: sounds like simply negating `modelSupportsImages`.
const imagesUnsupported = selectedImages.length > 0 && !modelSupportsImages

// ✅ Intent-revealing: conveys what will happen (warning/notice).
const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages
// or
const warnUnsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages

// ❗ Ensure canonical normalization is respected.
const menuPath = rawMenuPath.trim() // so comparisons/lookup match the runner’s behavior
``` 

Practical checklist:
- For booleans, ask: “Does this name describe the full meaning (e.g., ‘warning’) or only one component of the condition?”
- Prefer names like `warn...`, `unsupported...Attached`, `has...`, `should...` when the value drives UI behavior.
- Normalize/format any strings used for identifiers (paths, command names, menu paths) to match the canonical system so the name remains truthful.