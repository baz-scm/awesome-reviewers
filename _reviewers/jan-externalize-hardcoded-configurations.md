---
title: Externalize hardcoded configurations
description: Avoid hardcoding configuration values like ports, URLs, API endpoints,
  and environment-specific settings directly in source code. Instead, externalize
  these values to environment variables, configuration files, or dependency injection
  to improve maintainability and deployment flexibility.
repository: menloresearch/jan
label: Configurations
language: TypeScript
comments_count: 3
repository_stars: 37620
---

Avoid hardcoding configuration values like ports, URLs, API endpoints, and environment-specific settings directly in source code. Instead, externalize these values to environment variables, configuration files, or dependency injection to improve maintainability and deployment flexibility.

Hardcoded configurations make applications difficult to deploy across different environments and create tight coupling between code and environment-specific values.

**What to externalize:**
- Server ports and host addresses
- API endpoints and URLs  
- Database connection strings
- Feature flags and environment-specific settings
- API keys and secrets

**Example:**
```typescript
// ❌ Avoid: Hardcoded in source
const PORT = 1337;
const LOCAL_HOST = "127.0.0.1";
const JAN_HTTP_SERVER_URL = `http://${LOCAL_HOST}:${PORT}`;

// ✅ Better: Use environment variables
const PORT = process.env.JAN_API_PORT || 1337;
const LOCAL_HOST = process.env.JAN_HOST || "127.0.0.1";
const JAN_HTTP_SERVER_URL = `http://${LOCAL_HOST}:${PORT}`;
```

Move configuration values to `.env` files, environment variables, or inject them from the application layer rather than defining them in core modules. This enables different configurations for development, testing, and production environments without code changes.