---
title: Use structured logging
description: Always use the project's structured logger instead of direct console
  methods (`console.log`, `console.error`, etc.). This ensures consistent log formatting,
  proper level-based filtering, and integration with monitoring systems.
repository: n8n-io/n8n
label: Logging
language: TypeScript
comments_count: 8
repository_stars: 122978
---

Always use the project's structured logger instead of direct console methods (`console.log`, `console.error`, etc.). This ensures consistent log formatting, proper level-based filtering, and integration with monitoring systems.

**Problems with direct console logging:**
1. Bypasses log level controls (making it impossible to silence debug logs in production)
2. Creates inconsistent log formats that are harder to parse
3. Misses enrichment with contextual metadata
4. Bypasses centralized logging configuration

**Good logging practice:**
```typescript
// AVOID: Direct console logging
console.log('Database pool created'); // Hard to filter out in production
console.error('Error handling streaming chunk:', error); // Bypasses error tracking

// BETTER: Use the structured logger with appropriate levels
this.logger.debug('Database pool created'); // Can be silenced in production
this.logger.info(`Generated workflow for prompt: ${flags.prompt}`); // Informational messages
this.logger.warn('The output file already exists. It will be overwritten.'); // Warnings
this.logger.error(`Error processing prompt "${flags.prompt}": ${errorMessage}`); // Actual errors
```

For debug-only logging, conditionally log based on environment or debug flags rather than leaving console statements that will always execute:

```typescript
// BETTER: Conditional debug logging
if (isDebugMode) {
  this.logger.debug(`Connection parameters for ${nodeType}:`, warnings);
}
```

Ensure log levels match the message severity - use error only for actual failures, and info/debug for status messages to prevent false alarms in monitoring systems.