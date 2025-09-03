---
title: Consistent null safety patterns
description: Maintain consistent approaches to null and undefined handling throughout
  the codebase. Use optional chaining (`?.`) for safe property access, but be mindful
  that it may not always be equivalent to explicit type and null checks. When accessing
  properties on values that could be objects, always include explicit null checks
  alongside type checks since `typeof...
repository: ant-design/ant-design
label: Null Handling
language: TSX
comments_count: 5
repository_stars: 95882
---

Maintain consistent approaches to null and undefined handling throughout the codebase. Use optional chaining (`?.`) for safe property access, but be mindful that it may not always be equivalent to explicit type and null checks. When accessing properties on values that could be objects, always include explicit null checks alongside type checks since `typeof null === 'object'`. Avoid non-null assertion operators (`!`) and instead provide explicit fallback values.

Examples:
```typescript
// Good: Explicit null check with type check
onClose={typeof closable === 'object' && closable !== null ? closable.onClose : undefined}

// Good: Optional chaining for simple cases
if (selectable?.length > 0 && selectType) { ... }

// Good: Explicit fallback instead of non-null assertion
initExpandedKeys = props.expandedKeys || defaultExpandedKeys || [];

// Avoid: Non-null assertion without fallback
initExpandedKeys = (props.expandedKeys || defaultExpandedKeys)!;
```

Consider the semantic difference between optional chaining and explicit checks - optional chaining treats all falsy values the same way, while explicit checks allow for more nuanced handling of different null/undefined scenarios.