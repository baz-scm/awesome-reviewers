---
title: Robust comparison algorithms
description: 'Ensure your comparison algorithms handle edge cases properly and avoid
  common pitfalls:


  1. **Normalize values before comparison** - When comparing strings, consider if
  you need to normalize whitespace, case, or other variants:'
repository: continuedev/continue
label: Algorithms
language: TypeScript
comments_count: 5
repository_stars: 27819
---

Ensure your comparison algorithms handle edge cases properly and avoid common pitfalls:

1. **Normalize values before comparison** - When comparing strings, consider if you need to normalize whitespace, case, or other variants:

```typescript
// Problematic: Direct comparison may fail due to trailing whitespace
if (lineA === lineB) { /* ... */ }

// Better: Normalize before comparing when appropriate
if (lineA.trimEnd() === lineB.trimEnd()) { /* ... */ }
```

2. **Avoid variable shadowing in comparisons** - Be careful with variable names in loops and nested scopes:

```typescript
// Problematic: 'model' shadows the outer parameter
for (const model of specificModels) {
  if (model.toLowerCase() === model) { // Always true!
    return true;
  }
}

// Better: Use distinct variable names
for (const specificModel of specificModels) {
  if (model.toLowerCase() === specificModel.toLowerCase()) {
    return true;
  }
}
```

3. **Check termination conditions carefully** - Ensure loops don't break prematurely:

```typescript
// Problematic: Breaking loop on first non-match may skip valid items
for (let i = chatHistory.length - 1; i >= 0; i--) {
  if (item.message.role !== "assistant") {
    break; // Stops looking at earlier messages
  }
}

// Better: Continue searching when appropriate
for (let i = chatHistory.length - 1; i >= 0; i--) {
  if (item.message.role !== "assistant") {
    continue; // Skips this item but continues searching
  }
  // Process assistant messages
}
```

4. **Consider equality semantics** - Think about what "equal" means in your context (identity, content, references?):

```typescript
// Problematic: Strict equality might miss semantically equivalent items
if (i.id.providerTitle === item.id.providerTitle) {
  // Only checks exact IDs, might miss different references to same resource
}

// Better: Consider what equality means in this context
if ((i.id.providerTitle === item.id.providerTitle) ||
    (i.uri && item.uri && i.uri.value === item.uri.value)) {
  // Checks both ID equality and URI reference equality
}
```