---
title: Consistent semantic naming
description: 'Use clear, consistent, and semantic naming patterns across your codebase
  to improve readability and maintainability:


  1. **Start function names with verbs** that describe the action being performed:'
repository: vercel/ai
label: Naming Conventions
language: TypeScript
comments_count: 10
repository_stars: 15590
---

Use clear, consistent, and semantic naming patterns across your codebase to improve readability and maintainability:

1. **Start function names with verbs** that describe the action being performed:
```typescript
// Good
createProviderDefinedToolFactory()
parseJson()

// Avoid
providerDefinedToolFactory()
jsonParser()
```

2. **Use descriptive names for generics** rather than single letters:
```typescript
// Good
interface Provider<LANGUAGE extends string, CONTEXT extends string>

// Avoid
interface Provider<L extends string, C extends string>
```

3. **Follow consistent case conventions**:
   - Use camelCase for object properties and variables
   - Start non-class/type variables (including schemas) with lowercase
   - Use consistent naming across similar APIs

4. **Include units in variable names** to prevent ambiguity:
```typescript
// Good
durationInSeconds: number
maxParallelRequests: number

// Avoid
duration: number
concurrency: number
```

5. **Use standard terminology** in field names (e.g., `mediaType` for IANA media types)

6. **Ensure test naming matches implementation** to avoid confusion and maintenance issues

Following these conventions makes your code more self-documenting, easier to understand, and reduces the cognitive load for developers reading and maintaining the code.