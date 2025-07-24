---
title: Consistent message terminology
description: 'Use clear, consistent terminology in all error messages and user-facing
  text. Avoid technical jargon that might confuse users, and maintain consistency
  in language patterns across the codebase:'
repository: microsoft/typescript
label: Naming Conventions
language: Json
comments_count: 2
repository_stars: 105378
---

Use clear, consistent terminology in all error messages and user-facing text. Avoid technical jargon that might confuse users, and maintain consistency in language patterns across the codebase:

1. Use explicit wording instead of technical jargon
   - Prefer: "Enforce that mutable properties cannot satisfy 'readonly' requirements in assignments"
   - Avoid: "Ensure 'readonly' properties remain read-only in type relationships"

2. Maintain consistent language patterns
   - Use full forms instead of contractions ("are not" instead of "aren't")
   - Example:
     ```typescript
     // Preferred
     "Default imports are not allowed in a deferred import."
     
     // Avoid
     "Default imports aren't allowed for deferred imports."
     ```

Consistent terminology improves readability and maintains a professional style throughout the codebase.