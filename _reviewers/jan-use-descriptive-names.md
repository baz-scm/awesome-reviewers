---
title: Use descriptive names
description: Choose variable and function names that clearly communicate their purpose,
  type, and behavior. Names should be self-documenting and immediately understandable
  to other developers without requiring additional context.
repository: menloresearch/jan
label: Naming Conventions
language: TypeScript
comments_count: 3
repository_stars: 37620
---

Choose variable and function names that clearly communicate their purpose, type, and behavior. Names should be self-documenting and immediately understandable to other developers without requiring additional context.

For boolean variables and functions, use names that clearly indicate they return true/false values:
- Prefix with `is`, `has`, `can`, `should`, or similar indicators
- Use descriptive terms that make the boolean nature obvious

For properties and variables, prefer generic, maintainable names over product-specific ones, especially in open source projects where the codebase may be forked or renamed.

Examples:
```typescript
// Poor naming - unclear purpose
const SOME_API_KEY_ADDED = 'someApiKeyAdded'
const checkFileExists = (path: string) => boolean

// Better naming - clear purpose and type
const IS_ANY_REMOTE_MODEL_CONFIGURED = 'isAnyRemoteModelConfigured'
const exists = (path: string) => boolean

// Poor naming - product-specific
const properties = { JanVersion: VERSION }

// Better naming - generic and maintainable  
const properties = { appVersion: VERSION }
```

This approach improves code readability, reduces the need for comments, and makes the codebase more maintainable for both current and future developers.