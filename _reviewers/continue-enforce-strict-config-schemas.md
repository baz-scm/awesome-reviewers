---
title: Enforce strict config schemas
description: Configuration schemas should explicitly define all required fields and
  validate types at compile time to prevent runtime errors. Use strict typing with
  clear validation rules, and avoid marking required fields as optional.
repository: continuedev/continue
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 27819
---

Configuration schemas should explicitly define all required fields and validate types at compile time to prevent runtime errors. Use strict typing with clear validation rules, and avoid marking required fields as optional.

Example:
```typescript
// ❌ Problematic: Required field marked as optional
const configSchema = z.object({
  modelArn: z.string().optional(), // Could cause runtime errors
});

// ✅ Better: Explicit required/optional fields
const configSchema = z.object({
  modelArn: z.string(), // Required field
  profile: z.string().optional(), // Truly optional field
  region: z.string().optional(),
});

// Add runtime validation
function validateConfig(config: Config) {
  const result = configSchema.safeParse(config);
  if (!result.success) {
    throw new ValidationError(result.error.errors);
  }
}
```

This approach:
1. Makes required fields explicit in the schema
2. Catches missing required fields at compile time
3. Provides clear validation errors at runtime
4. Maintains consistency between schema and implementation