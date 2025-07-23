---
title: Maintain consistent terminology patterns
description: Ensure consistent terminology usage across the codebase, especially in
  localization files and technical documentation. When a term is established (whether
  in translation or technical context), maintain that same term throughout related
  files and contexts.
repository: RooCodeInc/Roo-Code
label: Naming Conventions
language: Json
comments_count: 7
repository_stars: 17288
---

Ensure consistent terminology usage across the codebase, especially in localization files and technical documentation. When a term is established (whether in translation or technical context), maintain that same term throughout related files and contexts.

Key guidelines:
1. Use identical technical terms across related contexts (e.g., if using "API key", don't switch to "API token")
2. Maintain consistent translations for technical terms across localization files
3. Preserve capitalization patterns for product/technical names
4. Use the same term for identical concepts across different languages

Example:
```json
// Incorrect - Inconsistent terminology
{
  "vectorStore": {
    "embeddings": "埋め込み次元",
    "dimensions": "ベクター次元"  // Inconsistent with embeddings
  }
}

// Correct - Consistent terminology
{
  "vectorStore": {
    "embeddings": "ベクター次元",
    "dimensions": "ベクター次元"  // Maintains consistency
  }
}
```

This practice improves code maintainability, reduces confusion, and ensures a more professional user experience, especially in localized applications.