---
title: "Consistent variable style patterns"
description: "Maintain consistent patterns for variable declarations and naming conventions: use const by default for variable declarations, use clear complete words in variable names instead of abbreviations, and for truthiness checks prefer simple boolean conditions unless explicit null/undefined checks are required."
repository: "vercel/next.js"
label: "Code Style"
language: "TypeScript"
comments_count: 3
repository_stars: 133000
---

Maintain consistent patterns for variable declarations and naming conventions:

1. Use `const` by default for variable declarations, only use `let` when the variable needs to be reassigned
2. Use clear, complete words in variable names instead of abbreviations
3. For truthiness checks, prefer simple boolean conditions unless explicit null/undefined checks are required

Example:
```typescript
// ❌ Inconsistent patterns
let lockFile = findRootLockFile(cwd)
const normChunkPath = '/path'
if (testWasmDir != null) {
  // ...
}

// ✅ Consistent patterns
const lockFile = findRootLockFile(cwd)
const normalizedChunkPath = '/path'
if (testWasmDir) {
  // ...
}
```

This promotes code readability and reduces cognitive load by establishing predictable patterns across the codebase.