---
title: Use structured error logging
description: Always use the proper logger instance instead of console methods, and
  format error logs with structured data objects rather than string concatenation.
  Console logging methods like `console.error` can lead to log flooding in production
  and lack proper log level controls. Structured logging with error objects enables
  better log parsing, monitoring, and...
repository: firecrawl/firecrawl
label: Logging
language: TypeScript
comments_count: 5
repository_stars: 54535
---

Always use the proper logger instance instead of console methods, and format error logs with structured data objects rather than string concatenation. Console logging methods like `console.error` can lead to log flooding in production and lack proper log level controls. Structured logging with error objects enables better log parsing, monitoring, and debugging.

**Avoid:**
```typescript
console.error('Schema validation error: Detected unconverted Zod schema');
logger.error(`Failed to scrape URL ${url}: ${scrapeResponse.error}`);
```

**Use instead:**
```typescript
logger.error('Schema validation error: Detected unconverted Zod schema', {
  type: val._def?.typeName,
  keys: Object.keys(val),
  hasZodProperties: !!(val._def || val.parse || val.safeParse)
});
logger.error(`Failed to scrape URL ${url}`, { error: scrapeResponse.error });
```

This approach provides consistent logging behavior across environments, enables proper log level filtering, and creates structured data that monitoring tools can easily parse and alert on.