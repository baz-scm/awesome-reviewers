---
title: Safe property access
description: Always use proper null safety patterns when accessing properties that
  might be null or undefined. This prevents runtime errors and improves code robustness.
repository: continuedev/continue
label: Null Handling
language: TSX
comments_count: 4
repository_stars: 27819
---

Always use proper null safety patterns when accessing properties that might be null or undefined. This prevents runtime errors and improves code robustness.

Key practices:
1. Use optional chaining consistently at every level of nested property access:
```typescript
// ❌ Inconsistent - still can cause runtime errors
configResult.config?.selectedModelByRole.chat?.completionOptions

// ✅ Consistent optional chaining
configResult.config?.selectedModelByRole?.chat?.completionOptions
```

2. Verify object type before accessing properties, especially with DOM elements:
```typescript
// ❌ Unsafe - activeElement could be null
document.activeElement.classList.contains("ProseMirror")

// ✅ Type-safe access
if (document.activeElement instanceof Element && 
    document.activeElement.classList.contains("ProseMirror"))
```

3. Use nullish coalescing to provide safe defaults:
```typescript
// ❌ Unsafe - will throw if nodeTextValue is null/undefined
startIndex = nodeTextValue.indexOf(query, startIndex);

// ✅ Safe with fallback
startIndex = nodeTextValue?.indexOf(query, startIndex) ?? -1;
```

4. Prefer positive conditions for null checks:
```typescript
// ❌ Less readable
onTitleClick={!item.content ? undefined : handleTitleClick}

// ✅ More readable
onTitleClick={item.content ? handleTitleClick : undefined}
```