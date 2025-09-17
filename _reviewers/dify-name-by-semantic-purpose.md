---
title: Name by semantic purpose
description: Choose names that reflect the semantic purpose and meaning rather than
  implementation details or arbitrary values. Use enum constants instead of string
  literals, select precise identifiers that clearly convey intent, and name functions/variables
  based on their actual purpose.
repository: langgenius/dify
label: Naming Conventions
language: TSX
comments_count: 4
repository_stars: 114231
---

Choose names that reflect the semantic purpose and meaning rather than implementation details or arbitrary values. Use enum constants instead of string literals, select precise identifiers that clearly convey intent, and name functions/variables based on their actual purpose.

Examples:
- Use `operationName === DocumentActionType.delete` instead of `operationName === 'delete'`
- Use `provider_type === 'local_file'` instead of checking multiple properties when a single semantic property exists
- Name functions like `handleUpload` instead of `handleImageCropped` when the function's purpose extends beyond just cropping
- Choose descriptive names like `'sketch'` instead of technical terms like `'handDrawn'`
- Define enums for related constants: `enum LookType { Classic = 'classic', Sketch = 'sketch' }`

This approach improves code readability, reduces magic strings, and makes the codebase more maintainable by clearly expressing the developer's intent.