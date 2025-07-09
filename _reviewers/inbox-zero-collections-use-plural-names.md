---
title: Collections use plural names
description: Always use plural names for properties representing collections (arrays/lists)
  in interfaces, types, and destructuring patterns. This ensures consistency between
  interface definitions and their usage throughout the codebase.
repository: elie222/inbox-zero
label: Naming Conventions
language: TSX
comments_count: 2
repository_stars: 8267
---

Always use plural names for properties representing collections (arrays/lists) in interfaces, types, and destructuring patterns. This ensures consistency between interface definitions and their usage throughout the codebase.

Example:
```typescript
// ❌ Inconsistent naming
interface DigestEmailProps {
  newsletter?: EmailItem[];  // singular for array
  receipt?: EmailItem[];     // singular for array
}

// ✅ Consistent plural naming
interface DigestEmailProps {
  newsletters?: EmailItem[];  // plural matches array type
  receipts?: EmailItem[];    // plural matches array type
}

// Usage remains consistent with interface
const { newsletters, receipts } = props;
```

This convention:
- Makes array types immediately recognizable
- Prevents confusion between single items and collections
- Reduces bugs from property name mismatches
- Follows common JavaScript/TypeScript conventions