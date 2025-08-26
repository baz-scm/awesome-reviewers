---
title: Ensure semantic naming clarity
description: Names should clearly convey their semantic purpose and avoid conflicts
  that reduce code readability. This applies to imports, types, variables, and methods.
repository: tree-sitter/tree-sitter
label: Naming Conventions
language: TypeScript
comments_count: 2
repository_stars: 21799
---

Names should clearly convey their semantic purpose and avoid conflicts that reduce code readability. This applies to imports, types, variables, and methods.

**Key principles:**
1. **Avoid naming conflicts**: When importing classes or types, choose names that don't conflict with local variables or other imports
2. **Use semantically distinct names**: Different concepts should have clearly distinguishable names, especially for related but different types
3. **Prioritize clarity over brevity**: Choose descriptive names that make the code's intent obvious

**Examples:**

Import naming to avoid conflicts:
```typescript
// Problematic - naming conflict
import Parser from 'web-tree-sitter';
const Parser: typeof Parser = await import('..').then(m => m.default);

// Better - clear, distinct names
import TSParser from 'web-tree-sitter';
const Parser: typeof TSParser = await import('..').then(m => m.default);
```

Type naming for semantic clarity:
```typescript
// Problematic - same interface for different concepts
interface QueryResult {
  pattern: number;
  captures: { name: string; node: SyntaxNode }[];
}

// Better - distinct names for different concepts
interface QueryMatch {
  pattern: number;
  captures: QueryCapture[];
}

interface QueryCapture {
  name: string;
  node: SyntaxNode;
}
```

This prevents confusion and makes the codebase more maintainable by ensuring each name has a clear, unambiguous meaning.