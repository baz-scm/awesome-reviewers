---
title: Maintain semantic naming consistency
description: 'Names should be semantically meaningful and consistent across related
  concepts in the codebase. This applies to variables, functions, components, and
  types. When naming:'
repository: n8n-io/n8n
label: Naming Conventions
language: TypeScript
comments_count: 4
repository_stars: 122978
---

Names should be semantically meaningful and consistent across related concepts in the codebase. This applies to variables, functions, components, and types. When naming:

1. Use consistent suffixes/prefixes for related concepts
2. Choose descriptive verbs for functions
3. Avoid abbreviations unless widely understood
4. Maintain naming patterns across similar features

Example of poor naming consistency:
```typescript
// Inconsistent naming pattern
interface User {
  customer_id: string;  // Uses _id suffix
  group: string;        // Missing _id suffix
}

function enableStreaminOption() {}  // Misspelled, unclear verb
```

Improved version:
```typescript
// Consistent naming pattern
interface User {
  customerId: string;   // Consistent camelCase
  groupId: string;      // Consistent naming pattern
}

function createStreamingOption() {}  // Clear verb, correct spelling
```

This helps maintain code readability and reduces cognitive load when working across different parts of the codebase.