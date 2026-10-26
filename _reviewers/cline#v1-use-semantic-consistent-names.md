---
title: Use semantic, consistent names
description: 'Use names that precisely describe what the value represents and keep
  shared concepts aligned with canonical representations.


  - For booleans, name after the condition they indicate (including when it’s derived
  from multiple inputs), not just a negated capability. Prefer positive, intention-revealing
  names.'
repository: cline/cline#v1
label: Naming Conventions
language: TSX
comments_count: 3
repository_stars: 70862
---

Use names that precisely describe what the value represents and keep shared concepts aligned with canonical representations.

- For booleans, name after the condition they indicate (including when it’s derived from multiple inputs), not just a negated capability. Prefer positive, intention-revealing names.
  - Example: rename
    - `const imagesUnsupported = selectedImages.length > 0 && !modelSupportsImages`
    - to `const unsupportedImagesAttached = selectedImages.length > 0 && !modelSupportsImages`
- For shared UI/identifiers, use the canonical imported component/variant (e.g., a lucide `<X />` component) instead of custom inline equivalents, so reviewers can quickly confirm consistency across the codebase.
- For naming/paths/command identifiers across layers, ensure you apply the same normalization rules consistently (e.g., trimming) so the names produced during inspection/menu building match what the runner/executor expects.

Result: code becomes easier to audit—readers can trust that the name matches the true meaning and that “same concept” is represented the same way everywhere.