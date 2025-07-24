---
title: Preserve naming consistency
description: 'Maintain consistent naming patterns and casing across all related code
  entities to ensure clarity and prevent errors. This includes:


  1. Use consistent casing for technical identifiers across all occurrences (in code,
  documentation, and translations)'
repository: microsoft/typescript
label: Naming Conventions
language: Other
comments_count: 3
repository_stars: 105378
---

Maintain consistent naming patterns and casing across all related code entities to ensure clarity and prevent errors. This includes:

1. Use consistent casing for technical identifiers across all occurrences (in code, documentation, and translations)
2. When entities are conceptually related (like types and namespaces sharing the same name), ensure naming consistency is maintained across all instances
3. When renaming an identifier, ensure all related occurrences are updated consistently

**Example:**
```typescript
// CORRECT: Consistent casing of 'checkJs' option
// In code:
compiler.options.checkJs = true;

// In documentation:
// "Use the 'checkJs' option to get errors from JavaScript files."

// CORRECT: Consistent naming across related entities
type Foo = number;
namespace Foo {
   export type U = string;
}
export = Foo;
// When renaming 'Foo', ensure it's renamed in all three places
```

Inconsistent naming leads to confusion, makes code harder to maintain, and can cause runtime errors when references don't match.