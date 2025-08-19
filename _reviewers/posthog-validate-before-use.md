---
title: validate before use
description: Always validate that values are truthy or defined before using them,
  even when they are expected to exist. This prevents runtime errors and unexpected
  behavior when assumptions about data presence are violated.
repository: PostHog/posthog
label: Null Handling
language: TypeScript
comments_count: 2
repository_stars: 28460
---

Always validate that values are truthy or defined before using them, even when they are expected to exist. This prevents runtime errors and unexpected behavior when assumptions about data presence are violated.

The pattern helps catch edge cases where expected values might be missing, null, or undefined, avoiding silent failures or unexpected default behaviors.

Example:
```typescript
// Instead of assuming properties exists
let properties = data.event.properties
if ('exception_props' in properties) {
    // use properties
}

// Validate it's truthy first
let properties = data.event.properties
if (properties && 'exception_props' in properties) {
    // use properties
}

// For expected values that might be missing
if (event.now) {
    const capturedAtDateTime = DateTime.fromISO(event.now).toUTC()
    preIngestionEvent.capturedAt = capturedAtDateTime.isValid ? capturedAtDateTime : undefined
}
```

This approach prevents scenarios like getting unexpected fallback values (e.g., "1970-01-01 00:00:00.000000" in databases) when validation fails silently.