---
title: Environment variable fallbacks
description: Always implement proper fallback chains for environment variables and
  handle missing configuration gracefully. When introducing new environment variables,
  maintain backward compatibility with existing ones, and apply environment-specific
  behavior conditionally to avoid issues across different deployment contexts.
repository: novuhq/novu
label: Configurations
language: TypeScript
comments_count: 5
repository_stars: 37700
---

Always implement proper fallback chains for environment variables and handle missing configuration gracefully. When introducing new environment variables, maintain backward compatibility with existing ones, and apply environment-specific behavior conditionally to avoid issues across different deployment contexts.

Key practices:
- Use fallback chains with multiple environment variable options
- Provide sensible defaults or graceful degradation when configuration is missing
- Apply conditional logic based on deployment environment (e.g., `IS_DOCKER_HOSTED`)
- Maintain backward compatibility when renaming environment variables

Example implementation:
```typescript
export function resolveLogging(providedLogging?: boolean): boolean {
  if (providedLogging !== undefined) {
    return providedLogging;
  }
  // Support both new and legacy environment variables
  if (process.env.LOGGING_LEVEL || process.env.LOG_LEVEL) {
    return (process.env.LOGGING_LEVEL || process.env.LOG_LEVEL) === 'true';
  }
  
  // Graceful fallback based on environment
  return !['test', 'production'].includes(process.env.NODE_ENV);
}

// Conditional behavior based on deployment context
const options = process.env.IS_DOCKER_HOSTED === 'true' 
  ? { priority: command.priority } 
  : {};
```

For optional services, avoid initialization entirely when configuration is missing rather than using empty defaults, allowing the application to bootstrap gracefully without the optional functionality.