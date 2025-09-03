---
title: Add explanatory comments
description: 'Code should include explanatory comments when the purpose, behavior,
  or context is not immediately clear from reading the code itself. This is especially
  important for:'
repository: angular/angular
label: Documentation
language: TypeScript
comments_count: 5
repository_stars: 98611
---

Code should include explanatory comments when the purpose, behavior, or context is not immediately clear from reading the code itself. This is especially important for:

- **Non-obvious implementation decisions**: When code deviates from expected patterns or removes common safeguards, explain why.
- **Complex data structures**: Interface fields, especially those with specific usage patterns or constraints, should be documented.
- **Important behavioral details**: When functionality has side effects or specific requirements that affect how it should be used.
- **Context-dependent logic**: Code that requires understanding of broader system behavior or migration patterns.

**Example:**
```typescript
// Before - unclear why early return was removed
if (ngDevMode) {
  // ... complex logic
}

// After - explains the reasoning
if (ngDevMode) {
  // Note: Early return removed to ensure proper cleanup in all code paths
  // ... complex logic
}

// Before - unclear field purpose
export interface ProjectedSignalNode {
  propertyNode: ReactiveNode | undefined;
  lastProperty: PropertyKey | undefined;
}

// After - explains field usage
export interface ProjectedSignalNode {
  // Only used when the projectedSignal key argument is reactive
  propertyNode: ReactiveNode | undefined;
  // Tracks the last accessed property for change detection
  lastProperty: PropertyKey | undefined;
}
```

Comments should focus on the "why" rather than the "what" - explaining the reasoning, constraints, or important context that future developers need to understand when modifying or using the code.