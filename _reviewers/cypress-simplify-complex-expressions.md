---
title: Simplify complex expressions
description: Break down complex conditional logic, nested structures, and verbose
  syntax into smaller, well-named functions or more concise expressions. This improves
  code readability and maintainability.
repository: cypress-io/cypress
label: Code Style
language: Other
comments_count: 5
repository_stars: 48850
---

Break down complex conditional logic, nested structures, and verbose syntax into smaller, well-named functions or more concise expressions. This improves code readability and maintainability.

Key practices:
- Extract complex nested if/else statements into descriptive helper functions
- Use modern, idiomatic JavaScript/TypeScript syntax where available
- Replace verbose type annotations with more concise alternatives
- Break complex boolean conditions into named predicates

Example of improvement:
```typescript
// Instead of complex nested conditions:
if (err && err.showDiff !== false && err.expected !== undefined && _sameType(err.actual, err.expected)) {
  // ...
}

// Extract into named functions:
const diffCanBeShown = (err) => err && err.showDiff !== false
const hasExpectedValue = (err) => err.expected !== undefined
const hasSameTypeValues = (err) => _sameType(err.actual, err.expected)

const showDiff = (err) => diffCanBeShown(err) && hasExpectedValue(err) && hasSameTypeValues(err)
```

Also prefer concise TypeScript syntax:
```typescript
// Instead of: const docsMenuVariant: Ref<DocsMenuVariant> = ref('main')
const docsMenuVariant = ref<DocsMenuVariant>('main')
```

And use idiomatic JavaScript methods:
```typescript
// Instead of: indexOf() !== -1
// Use: includes()
```