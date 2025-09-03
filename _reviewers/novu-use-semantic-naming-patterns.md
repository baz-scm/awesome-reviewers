---
title: Use semantic naming patterns
description: Establish consistent naming conventions that preserve semantic meaning
  and follow established patterns. Use descriptive names that clearly indicate purpose
  and type.
repository: novuhq/novu
label: Naming Conventions
language: TypeScript
comments_count: 6
repository_stars: 37700
---

Establish consistent naming conventions that preserve semantic meaning and follow established patterns. Use descriptive names that clearly indicate purpose and type.

Key guidelines:
- Suffix enums with "Enum" for consistency: `SeverityLevelEnum` instead of `SeverityLevel`
- Prefix boolean functions with semantic indicators: `shouldLogAnalytics()` instead of `isLogAnalytics()`
- Use semantic names in iterations: `map((variable) => ...)` instead of `map((error) => ...)`
- Avoid confusing terms in class names: `WorkflowStepFetcher` instead of `StepTemplateFetcher`
- Preserve original casing in user-facing suggestions: use `searchText` instead of `searchLower` for variable name suggestions
- Maintain consistent parameter naming across similar functions: stick to `workflowId` rather than mixing `workflowIdOrInternalId`

Example:
```typescript
// Good
export enum SeverityLevelEnum { ... }
function shouldLogAnalytics(): boolean { ... }
invalidVariables.map((variable) => ({ message: variable.name }))

// Avoid  
export enum SeverityLevel { ... }
function isLogAnalytics(): boolean { ... }
invalidVariables.map((error) => ({ message: error.name }))
```

This ensures code is self-documenting and maintains consistency across the codebase.