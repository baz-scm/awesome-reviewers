---
title: Validate nullable values explicitly
description: Always handle potentially null or undefined values explicitly using type
  guards, null coalescing operators, and proper fallback values. This ensures type
  safety and prevents runtime errors from null references.
repository: RooCodeInc/Roo-Code
label: Null Handling
language: TypeScript
comments_count: 7
repository_stars: 17288
---

Always handle potentially null or undefined values explicitly using type guards, null coalescing operators, and proper fallback values. This ensures type safety and prevents runtime errors from null references.

Key practices:
1. Use the nullish coalescing operator (??) instead of OR (||) when 0 or empty string are valid values:
```typescript
// Good
const reservedTokens = maxTokens ?? DEFAULT_TOKENS
// Bad - will override 0 with default
const reservedTokens = maxTokens || DEFAULT_TOKENS
```

2. Add explicit type guards when checking object properties:
```typescript
// Good
if (typeof data === "object" && data !== null && "property" in data) {
  return data.property
}
// Bad
return data?.property || defaultValue
```

3. Provide explicit fallbacks for optional values:
```typescript
// Good
const description = mode.description ?? mode.whenToUse ?? mode.roleDefinition ?? ''
// Bad
const description = mode.description || mode.whenToUse || mode.roleDefinition
```

This approach prevents subtle bugs from implicit type coercion and makes null handling intentions clear in the code.