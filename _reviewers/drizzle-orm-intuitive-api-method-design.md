---
title: intuitive API method design
description: Design API methods with intuitive names and signatures that follow established
  conventions and provide good ergonomics. Avoid method names that conflict with well-known
  patterns from other domains, and prefer streamlined method signatures that reduce
  unnecessary verbosity.
repository: drizzle-team/drizzle-orm
label: API
language: TypeScript
comments_count: 2
repository_stars: 29461
---

Design API methods with intuitive names and signatures that follow established conventions and provide good ergonomics. Avoid method names that conflict with well-known patterns from other domains, and prefer streamlined method signatures that reduce unnecessary verbosity.

Key principles:
- Avoid overloading method names that have established meanings (e.g., `.then()` is associated with Promises)
- Design method signatures to accept parameters directly when possible, rather than requiring wrapper functions
- Consider alternative naming that better reflects the method's purpose

Example of problematic naming:
```typescript
// Confusing - .then() suggests Promise-like behavior
caseWhen(condition).then(value)

// Better - clearer intent
when(condition, value)
```

Example of improved method signature:
```typescript
// Verbose - requires unnecessary type wrapper
literalSchema.or(type('unknown.any[] | Record<string, unknown.any>'))

// Streamlined - accepts definition directly
literalSchema.or('unknown.any[] | Record<string, unknown.any>')
```

This approach makes APIs more discoverable, reduces cognitive load for developers, and prevents confusion with established patterns from other libraries or language features.