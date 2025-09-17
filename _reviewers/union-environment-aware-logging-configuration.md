---
title: Environment-aware logging configuration
description: Configure logging behavior dynamically based on the current environment
  to ensure appropriate log levels and destinations for development, staging, and
  production contexts. Development environments should use verbose logging (Trace/Debug)
  for debugging, while production should use minimal logging (Warning/Error) for performance.
  External logging services...
repository: unionlabs/union
label: Logging
language: TypeScript
comments_count: 2
repository_stars: 74800
---

Configure logging behavior dynamically based on the current environment to ensure appropriate log levels and destinations for development, staging, and production contexts. Development environments should use verbose logging (Trace/Debug) for debugging, while production should use minimal logging (Warning/Error) for performance. External logging services should be conditionally initialized to avoid unnecessary overhead in development.

Example implementation:
```typescript
const minimumLogLevel = Logger.minimumLogLevel(
  Match.value(ENV()).pipe(
    Match.when("DEVELOPMENT", () => LogLevel.Trace),
    Match.when("STAGING", () => LogLevel.Debug), 
    Match.when("PRODUCTION", () => LogLevel.Warning),
    Match.exhaustive,
  ),
)

const init = () => {
  if (ENV() === "DEVELOPMENT") {
    return // Skip external service initialization
  }
  
  // Initialize external logging service for staging/production
  externalLogger.init(config)
}
```

This approach ensures optimal logging performance across environments while maintaining debugging capabilities where needed.