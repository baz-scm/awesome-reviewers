---
title: Validate environment variables strictly
description: Enforce strict validation of environment variables using Zod schemas
  with explicit environment-specific rules. Required configurations should be mandatory
  in production while allowing flexibility in development/test environments.
repository: elie222/inbox-zero
label: Configurations
language: TypeScript
comments_count: 7
repository_stars: 8267
---

Enforce strict validation of environment variables using Zod schemas with explicit environment-specific rules. Required configurations should be mandatory in production while allowing flexibility in development/test environments.

Key principles:
1. Mark critical variables as required in production
2. Provide clear error messages for missing configurations
3. Allow optional values only in development/test
4. Implement proper fallback mechanisms for optional configs

Example:
```typescript
export const env = createEnv({
  server: {
    STRIPE_SECRET_KEY: z.string().refine(
      (val) => process.env.NODE_ENV === 'test' || !!val,
      'Missing STRIPE_SECRET_KEY in production',
    ),
    REDIS_URL: z.string().refine(
      (val) => process.env.NODE_ENV === 'test' || !!val,
      'Missing REDIS_URL in production',
    ),
    // Optional in all environments
    LOG_LEVEL: z.string().optional(),
  },
  client: {
    // Required in all environments
    NEXT_PUBLIC_API_URL: z.string().min(1),
  },
  // Validate on app startup
  runtimeEnv: process.env,
});
```

This approach prevents silent misconfigurations in production while maintaining development flexibility and providing clear error messages when required variables are missing.