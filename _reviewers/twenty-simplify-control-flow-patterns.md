---
title: simplify control flow patterns
description: 'Improve code readability by simplifying control flow structures and
  avoiding unnecessary complexity. This involves three key practices:


  **1. Use early returns instead of nested if/else blocks:**'
repository: twentyhq/twenty
label: Code Style
language: TypeScript
comments_count: 12
repository_stars: 35477
---

Improve code readability by simplifying control flow structures and avoiding unnecessary complexity. This involves three key practices:

**1. Use early returns instead of nested if/else blocks:**
```typescript
// Avoid nested structures
if (condition) {
  // logic
} else {
  // more logic
}

// Prefer early returns
if (!condition) {
  return earlyResult;
}
// main logic continues
```

**2. Break complex logic into smaller, named functions:**
```typescript
// Instead of complex nested logic
const getFieldFromSchema = (fieldKey: string, schema: RecordFieldNodeValue) => {
  return isRecordOutputSchemaV2(schema)
    ? schema.fields[fieldKey]
    : schema[fieldKey];
};
```

**3. Use appropriate language constructs:**
```typescript
// Use find() instead of manual loops
const contentType = Object.entries(headers)
  .find(([key]) => key.toLowerCase() === 'content-type')?.[1];

// Use simple comparisons instead of array includes for basic checks
if (depth > MAX_DEPTH) // instead of [0, 1, MAX_DEPTH].includes(depth)
```

These patterns make code easier to follow, reduce cognitive load, and minimize the chance of errors. Nested if/else structures are particularly hard to read and maintain, while early returns create a clear flow where exceptional cases are handled first, leaving the main logic unindented and easy to follow.