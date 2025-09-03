---
title: Environment variable access
description: Use direct `process.env` access and standardized configuration management
  instead of custom environment variable wrappers. Avoid redundant abstraction layers
  when the framework or libraries already handle environment variable inference automatically.
repository: lobehub/lobe-chat
label: Configurations
language: TypeScript
comments_count: 8
repository_stars: 65138
---

Use direct `process.env` access and standardized configuration management instead of custom environment variable wrappers. Avoid redundant abstraction layers when the framework or libraries already handle environment variable inference automatically.

**Key principles:**
- Use direct `process.env.VARIABLE_NAME` instead of custom env objects when possible
- Leverage `@t3-oss/env-nextjs` package for environment variable validation and type safety
- Follow standard naming conventions: `ENABLED_XXX` for feature flags and `XXX_API_KEY` for API keys
- Centralize environment configuration in dedicated config files (e.g., `src/config/app.ts`)
- Let frameworks handle automatic environment variable inference (e.g., next-auth automatically reads `AUTH_XXX` variables)

**Example:**
```typescript
// ❌ Avoid custom wrappers when direct access works
clientId: authEnv.AUTH_GOOGLE_CLIENT_ID ?? process.env.AUTH_GOOGLE_CLIENT_ID

// ✅ Use direct access for new implementations
clientId: process.env.AUTH_GOOGLE_CLIENT_ID

// ✅ Use @t3-oss/env-nextjs for validation
import { createEnv } from '@t3-oss/env-nextjs';

export const appEnv = createEnv({
  server: {
    ENABLED_CLOUDFLARE: z.boolean().default(false),
    CLOUDFLARE_API_KEY: z.string().optional(),
  }
});
```

This approach reduces complexity, improves maintainability, and leverages existing framework capabilities for environment variable management.