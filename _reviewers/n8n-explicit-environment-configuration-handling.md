---
title: Explicit environment configuration handling
description: 'Environment and configuration values should be explicit, visible, and
  environment-aware. Avoid hardcoded production values, hidden configuration properties,
  and complex environment variable logic. Instead:'
repository: n8n-io/n8n
label: Configurations
language: TypeScript
comments_count: 4
repository_stars: 122978
---

Environment and configuration values should be explicit, visible, and environment-aware. Avoid hardcoded production values, hidden configuration properties, and complex environment variable logic. Instead:

1. Use clear environment variable defaults:
```typescript
// Bad
export const skipAuth = process.env.SKIP_AUTH !== 'false';

// Good
export const skipAuth = process.env.SKIP_AUTH === 'true' || false;
```

2. Make configuration properties visible and customizable:
```typescript
// Bad
class Config {
  @Env('DB_NAME')
  database: string = 'production_db';  // Hardcoded production value
}

// Good
class Config {
  @Env('DB_NAME')
  database: string = 'local_db';  // Development-friendly default

  @Env('API_URL')
  apiUrl: string = 'http://localhost:3000';  // Visible and configurable
}
```

3. Ensure paths resolve in all environments:
```typescript
// Bad
const DIST_DIR = join(__dirname, '..', '..', '..', 'packages/frontend/dist');

// Good
const DIST_DIR = process.env.DIST_DIR || join(__dirname, 'dist');
```

This approach improves maintainability, prevents production issues, and makes configuration more transparent for developers and operators.