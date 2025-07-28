---
title: classify errors appropriately
description: 'Different types of errors require different handling strategies. Classify
  errors into categories and apply appropriate response patterns: fail fast for user-actionable
  problems, retry with backoff for transient issues, and graceful degradation for
  non-critical failures.'
repository: google-gemini/gemini-cli
label: Error Handling
language: TypeScript
comments_count: 5
repository_stars: 65062
---

Different types of errors require different handling strategies. Classify errors into categories and apply appropriate response patterns: fail fast for user-actionable problems, retry with backoff for transient issues, and graceful degradation for non-critical failures.

**Error Classification Guidelines:**
- **Client errors (4xx except 429)**: Fail fast - these indicate user or configuration problems that won't resolve with retries
- **Network/timeout errors**: Retry with exponential backoff - these are often transient
- **Server errors (5xx) and rate limits (429)**: Retry with backoff - server may recover
- **User-facing functionality**: Fail fast so users know when features aren't working
- **Background/telemetry operations**: Graceful degradation to avoid disrupting core functionality

**Example Implementation:**
```typescript
const shouldRetry = (err) => {
  // Network errors - retry
  if (!err.statusCode) return true;
  
  // Rate limits and server errors - retry  
  if (err.statusCode === 429 || err.statusCode >= 500) return true;
  
  // Client errors - fail fast
  return false;
};

// For user-facing features - fail fast
if (userWantsTelemetry && !telemetryWorking) {
  throw new Error('Telemetry failed - user should know');
}

// For background operations - graceful degradation
try {
  await backgroundTelemetry();
} catch (error) {
  console.debug('Background telemetry failed:', error);
  // Continue execution
}
```

This approach prevents infinite retry loops on permanent failures while ensuring transient issues are handled gracefully and users are informed when they need to take action.