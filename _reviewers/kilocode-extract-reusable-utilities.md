---
title: extract reusable utilities
description: When you notice repeated logic or functions that could be shared across
  multiple files, extract them into dedicated utility files. This improves code organization,
  reduces duplication, and minimizes merge conflicts.
repository: kilo-org/kilocode
label: Code Style
language: TypeScript
comments_count: 6
repository_stars: 7302
---

When you notice repeated logic or functions that could be shared across multiple files, extract them into dedicated utility files. This improves code organization, reduces duplication, and minimizes merge conflicts.

Key principles:
- Move helper functions to separate files rather than adding them to existing large files
- Create utility modules for commonly used logic patterns
- Avoid unnecessary indirection - only extract when there's genuine reuse or organizational benefit

Example:
```typescript
// Instead of adding to existing file
// src/core/prompts/system.ts
function getMorphInstructions(cwd: string, supportsComputerUse: boolean, settings?: Record<string, any>): string {
  // implementation
}

// Extract to dedicated utility
// src/utils/morph-instructions.ts
export function getMorphInstructions(cwd: string, supportsComputerUse: boolean, settings?: Record<string, any>): string {
  // implementation
}
```

This approach keeps files focused, reduces the likelihood of merge conflicts, and makes shared functionality more discoverable and maintainable.