---
title: Use descriptive constants
description: Replace hardcoded strings, numbers, and magic values with well-named
  constants that clearly describe their purpose and meaning. This improves code readability,
  maintainability, and reduces the risk of typos when the same values are used in
  multiple places.
repository: argoproj/argo-cd
label: Naming Conventions
language: TSX
comments_count: 5
repository_stars: 20149
---

Replace hardcoded strings, numbers, and magic values with well-named constants that clearly describe their purpose and meaning. This improves code readability, maintainability, and reduces the risk of typos when the same values are used in multiple places.

For string literals that are reused across the codebase, extract them into named constants:

```typescript
// Instead of:
if (info.name === 'Requests (CPU)') {
    // ...
}
if (info.name === 'Requests (MEM)') {
    // ...
}

// Use:
const RESOURCE_NAMES = {
    CPU_REQUESTS: 'Requests (CPU)',
    MEMORY_REQUESTS: 'Requests (MEM)'
} as const;

if (info.name === RESOURCE_NAMES.CPU_REQUESTS) {
    // ...
}
```

For magic numbers, use descriptive constants with explanatory comments when the logic isn't immediately obvious:

```typescript
// Instead of:
message += ' (' + revision.substring(0, 14) + ')';

// Use:
const SHA256_PREFIX_LENGTH = 8; // "sha256: " prefix
const DIGEST_DISPLAY_LENGTH = 7; // First 7 characters of actual digest
const TOTAL_DISPLAY_LENGTH = SHA256_PREFIX_LENGTH + DIGEST_DISPLAY_LENGTH;
message += ' (' + revision.substring(0, TOTAL_DISPLAY_LENGTH) + ')';
```

Additionally, ensure that variable and component names accurately reflect their actual functionality rather than misleading developers about their purpose.