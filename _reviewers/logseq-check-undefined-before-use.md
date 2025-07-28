---
title: Check undefined before use
description: Always verify that values are not undefined before accessing or using
  them, whether they are object properties or function parameters. This prevents TypeScript
  compilation errors and potential runtime issues.
repository: logseq/logseq
label: Null Handling
language: TSX
comments_count: 2
repository_stars: 37695
---

Always verify that values are not undefined before accessing or using them, whether they are object properties or function parameters. This prevents TypeScript compilation errors and potential runtime issues.

When accessing object properties that may not exist, use conditional checks or optional chaining. When dealing with function parameters that could be undefined, ensure proper type handling and validation.

Example from the codebase:
```typescript
// Before: Direct property access (causes TS error)
<TablerIcon name="text" />

// After: Check existence before use
<TablerIcon name={shape.props.label || shape.props.text ? "forms" : "text"} />

// For function parameters, ensure types handle undefined:
// Instead of assuming 'color' exists, fix types in ColorInput to handle undefined values
```

This practice ensures type safety and prevents unexpected behavior when values might be missing or undefined.