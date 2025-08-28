---
title: Simplify conditional logic
description: Prefer concise conditional expressions over verbose nested conditions
  and unnecessary boolean variables. This improves readability and reduces cognitive
  overhead.
repository: cloudflare/workers-sdk
label: Code Style
language: TypeScript
comments_count: 4
repository_stars: 3379
---

Prefer concise conditional expressions over verbose nested conditions and unnecessary boolean variables. This improves readability and reduces cognitive overhead.

**Key practices:**
- Combine multiple related conditions into a single statement
- Remove redundant type checks when more specific checks are sufficient
- Use direct assignment instead of conditional blocks when possible
- Eliminate unnecessary boolean variables in favor of direct control flow

**Examples:**

Instead of nested conditions:
```typescript
if (binding.binding && typeof binding.binding === "string") {
    if (binding.binding.toUpperCase() === normalizedName) {
        return true;
    }
}
```

Combine into single condition:
```typescript
if (typeof binding.binding === "string" && binding.binding.toUpperCase() === normalizedName) {
    return true;
}
```

Instead of boolean tracking variables:
```typescript
let isValid = false;
while (!isValid) {
    // validation logic
    if (validation.valid) {
        isValid = true;
    }
}
```

Use direct control flow:
```typescript
while (true) {
    // validation logic
    if (validation.valid) {
        return bindingName;
    }
}
```

Instead of conditional assignment:
```typescript
if (match) {
    const cachedAssetKey = await match.text();
    if (cachedAssetKey === assetKey) {
        shouldUpdateCache = false;
    }
}
```

Use direct assignment:
```typescript
if (match) {
    const cachedAssetKey = await match.text();
    shouldUpdateCache = cachedAssetKey !== assetKey;
}
```