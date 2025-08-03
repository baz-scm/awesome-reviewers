---
title: Maintain consistent naming patterns
description: 'Use consistent naming patterns throughout the codebase. When adding
  new identifiers, follow existing patterns in similar contexts. This includes:


  1. Consistent prefix/suffix patterns in related identifiers'
repository: RooCodeInc/Roo-Code
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 17288
---

Use consistent naming patterns throughout the codebase. When adding new identifiers, follow existing patterns in similar contexts. This includes:

1. Consistent prefix/suffix patterns in related identifiers
2. Consistent casing (camelCase, PascalCase, etc.)
3. Consistent naming patterns for configuration keys and constants

Example of inconsistent naming:
```typescript
// Inconsistent - mixing patterns
alwaysAllowReadOnly: true,
alwaysAllowWrite: true,
alwaysApproveResubmit: true,  // Should be alwaysAllowResubmit

// Inconsistent casing
const getLmStudioModels = ...
const getLMStudioModels = ...  // Inconsistent LM vs LM

// Inconsistent constant naming pattern
const SEARCH_MIN_SCORE = 0.4
const DEFAULT_MAX_SEARCH_RESULTS = 50  // Pattern mismatch
```

Corrected version:
```typescript
// Consistent prefix pattern
alwaysAllowReadOnly: true,
alwaysAllowWrite: true,
alwaysAllowResubmit: true,  // Follows established pattern

// Consistent casing
const getLMStudioModels = ...  // Standardized on LM
const getLMStudioModels = ...

// Consistent constant naming pattern
const DEFAULT_SEARCH_MIN_SCORE = 0.4
const DEFAULT_MAX_SEARCH_RESULTS = 50  // Consistent pattern
```

When adding new identifiers:
1. Look for similar existing identifiers and follow their pattern
2. Maintain consistent casing for acronyms (e.g., API, LM, URL)
3. Use consistent prefixes/suffixes for related configurations
4. Follow established patterns for constants and configuration keys