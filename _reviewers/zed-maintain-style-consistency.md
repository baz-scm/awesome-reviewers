---
title: Maintain style consistency
description: 'Ensure consistent styling is maintained across related elements in the
  codebase. This applies to:


  1. **Visual assets**: Icons and images should match the established dimensions and
  styling of existing assets.'
repository: zed-industries/zed
label: Code Style
language: Other
comments_count: 3
repository_stars: 62119
---

Ensure consistent styling is maintained across related elements in the codebase. This applies to:

1. **Visual assets**: Icons and images should match the established dimensions and styling of existing assets.
   ```
   // Example: All AI lab icons should be 16x16px
   ```

2. **Related file types**: When modifying style rules in one file, apply corresponding changes to related files of similar types.
   ```
   // When changing highlights in javascript/highlights.scm:
   (regex_flags) @keyword.operator.regex
   
   // Also update in typescript/highlights.scm and tsx/highlights.scm
   ```

3. **Semantic naming**: Use naming conventions that are logically consistent and avoid contradictory terminology. Ensure naming choices align with the conceptual understanding of the elements they represent.

Maintaining consistency improves readability, reduces confusion, and creates a more professional codebase that's easier to maintain over time.