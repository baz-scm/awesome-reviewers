---
title: Extract shared code patterns
description: Identify and extract duplicate code patterns into shared utility functions
  to improve maintainability and reduce redundancy. When similar logic appears in
  multiple places, create a reusable function in a shared utility file.
repository: RooCodeInc/Roo-Code
label: Code Style
language: TypeScript
comments_count: 5
repository_stars: 17288
---

Identify and extract duplicate code patterns into shared utility functions to improve maintainability and reduce redundancy. When similar logic appears in multiple places, create a reusable function in a shared utility file.

Example of problematic code:
```typescript
// In openai.ts
private isInsufficientQuotaError(error: any): boolean {
    // Duplicate quota detection logic
}

// In openai-compatible.ts
private isInsufficientQuotaError(error: any): boolean {
    // Same quota detection logic repeated
}
```

Better approach:
```typescript
// In shared/quota-utils.ts
export function isInsufficientQuotaError(error: any): boolean {
    // Centralized quota detection logic
}

// In both files:
import { isInsufficientQuotaError } from '../shared/quota-utils';
```

Key guidelines:
- Look for repeated logic patterns across files
- Extract shared functionality into well-named utility functions
- Place utilities in appropriate shared locations
- Document the purpose and usage of shared utilities
- Consider making utilities generic enough for reuse but specific enough to maintain clear purpose

This improves code maintainability by:
- Reducing duplicate code that needs to be maintained
- Centralizing logic for easier updates
- Making the codebase more DRY (Don't Repeat Yourself)
- Improving testability of shared functionality