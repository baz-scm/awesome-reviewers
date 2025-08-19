---
title: Environment-based configuration management
description: Prefer environment variables over file mounting for configuration values,
  and avoid hardcoded environment-specific conditionals like `isCloud()`. Instead,
  rely purely on configuration environment variables that can be set differently across
  environments. When setting default configuration values, consider the constraints
  and limits of downstream systems to...
repository: PostHog/posthog
label: Configurations
language: TypeScript
comments_count: 2
repository_stars: 28460
---

Prefer environment variables over file mounting for configuration values, and avoid hardcoded environment-specific conditionals like `isCloud()`. Instead, rely purely on configuration environment variables that can be set differently across environments. When setting default configuration values, consider the constraints and limits of downstream systems to prevent runtime failures.

For example, instead of:
```typescript
sslOptions: isCloud()
    ? {
          ca: fs.readFileSync(join(__dirname, '../cassandra/ca.crt')),
      }
    : undefined
```

Use environment variables:
```typescript
sslOptions: process.env.CASSANDRA_SSL_CA
    ? {
          ca: Buffer.from(process.env.CASSANDRA_SSL_CA, 'base64'),
      }
    : undefined
```

And when setting defaults, consider system limits:
```typescript
// Consider Kafka's 1MB limit when setting defaults
PERSON_PROPERTIES_SIZE_LIMIT: 512 * 1024, // 512KB default (safe margin under 1MB Kafka limit)
```

This approach makes configuration more flexible, testable, and avoids deployment complexities like file mounting while ensuring defaults don't cause system failures.