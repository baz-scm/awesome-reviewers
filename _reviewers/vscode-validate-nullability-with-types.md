---
title: Validate nullability with types
description: Always handle null and undefined values explicitly through proper type
  declarations and validation patterns rather than using non-null assertions or unsafe
  type casts. This ensures type safety and prevents runtime errors.
repository: microsoft/vscode
label: Null Handling
language: TypeScript
comments_count: 10
repository_stars: 174887
---

Always handle null and undefined values explicitly through proper type declarations and validation patterns rather than using non-null assertions or unsafe type casts. This ensures type safety and prevents runtime errors.

Key practices:
1. Use type declarations to make nullability explicit
2. Implement proper validation before accessing potentially null values
3. Prefer assignment patterns over non-null assertions
4. Use type-safe alternatives like optional chaining and nullish coalescing

Example:

```typescript
// ❌ Avoid
function processItem(item: Item | undefined) {
    return item!.value; // Unsafe non-null assertion
}

// ✅ Better
function processItem(item: Item | undefined) {
    if (!item) {
        return undefined;
    }
    return item.value;
}

// ✅ Even better - using type guards
function processItem(item: Item | undefined): string | undefined {
    if (isValidItem(item)) {
        return item.value;
    }
    return undefined;
}

// ✅ Best - with proper typing and validation
interface ItemProcessor {
    process(item: Item): string;
}

class SafeItemProcessor implements ItemProcessor {
    process(item: Item): string {
        // Type system ensures item is never null/undefined
        return item.value;
    }
}
```