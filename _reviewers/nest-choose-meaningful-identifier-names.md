---
title: Choose meaningful identifier names
description: 'Names for variables, methods, and classes should be descriptive, semantically
  accurate, and consistent with established conventions. Follow these guidelines:'
repository: nestjs/nest
label: Naming Conventions
language: TypeScript
comments_count: 9
repository_stars: 71767
---

Names for variables, methods, and classes should be descriptive, semantically accurate, and consistent with established conventions. Follow these guidelines:

1. Use names that clearly describe the purpose or content:
   ```typescript
   // Bad
   const val: any = getValue();
   
   // Good
   const fileOrFiles: File | File[] = getUploadedFiles();
   ```

2. Follow semantic naming conventions:
   - Boolean variables/methods should use "is", "has", or "should" prefixes
   - Error classes should be specific (e.g., `RouterAliasError` instead of `Error`)
   - Maintain consistent pluralization (e.g., `PostsService` for a service handling multiple posts)

3. Align with framework and library conventions:
   - Match external library naming patterns when extending their functionality
   - Follow project's established naming patterns for consistency
   - Preserve meaningful naming from referenced libraries

4. Avoid generic or ambiguous names:
   - Replace generic names like 'data', 'value', 'info' with context-specific alternatives
   - Use type-specific prefixes/suffixes when appropriate
   - Consider the scope and usage when choosing names

Remember that good names serve as self-documentation and improve code maintainability.