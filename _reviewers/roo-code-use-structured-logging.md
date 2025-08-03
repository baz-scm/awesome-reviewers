---
title: Use structured logging
description: Replace direct `console.log`, `console.warn`, and `console.error` calls
  with a centralized logging abstraction. This ensures logs are consistently formatted,
  properly categorized by severity, and can be filtered or disabled in production
  environments.
repository: RooCodeInc/Roo-Code
label: Logging
language: TypeScript
comments_count: 5
repository_stars: 17288
---

Replace direct `console.log`, `console.warn`, and `console.error` calls with a centralized logging abstraction. This ensures logs are consistently formatted, properly categorized by severity, and can be filtered or disabled in production environments.

**Benefits:**
- Consistent log format across the codebase
- Ability to control log verbosity by level
- Easier to add metadata to log entries
- Can be redirected to different outputs or monitoring services

**Implementation:**
1. Create or use an existing logging service/abstraction
2. Use appropriate logging levels based on the message purpose:
   - `logger.debug()` - For development-only information
   - `logger.info()` - For normal operational messages
   - `logger.warn()` - For concerning but non-critical issues
   - `logger.error()` - For failures that require attention

**Example:**

Instead of:
```typescript
console.log("[CodeIndexManager] Attempting to recover from error state before starting indexing.")
console.log("APi Protocol:", apiProtocol)
console.error(`Error parsing Ollama models response: ${JSON.stringify(parsedResponse.error, null, 2)}`)
```

Use a logger:
```typescript
logger.info("[CodeIndexManager] Attempting to recover from error state before starting indexing.")
logger.debug("API Protocol:", apiProtocol)
logger.error("Error parsing Ollama models response:", { error: parsedResponse.error })
```